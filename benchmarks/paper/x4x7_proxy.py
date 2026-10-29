"""A fault-injection proxy for X7: sits between wardowl and a server, and misbehaves on request.

    python benchmarks/paper/x4x7_proxy.py --kind http --listen 127.0.0.1:18080 \
        --upstream 127.0.0.1:8080 --admin 127.0.0.1:19080

`--kind http` understands HTTP/1.1 (keep-alive, Content-Length and chunked bodies) and can rewrite
answers; `--kind tcp` forwards bytes (for Postgres) and can only refuse, hold or delay them. The mode
is set through the admin port: `POST /mode` with `{"mode": "slow", "delay_ms": 1000}`; `GET /mode`
returns it; `GET /health` answers 200. Modes:

* `pass`: forward unchanged.
* `refuse`: close the listener and every open connection, so connections are refused.
* `blackhole`: accept connections and read requests, never answer; leaving the mode closes them.
* `slow`: wait `delay_ms` before forwarding each request (http) or each chunk of the answer (tcp).
* `http500`, `http503`: answer every request with that status (http only).
* `truncate`, `empty`, `garbage-json`, `type-flip`, `drop-last`, `allow-all`: forward, then alter
  the answer (http only): cut in half; an empty body; `{"unexpected": true}`; booleans as strings and
  decision enums as an unknown value; the last element of the answer's list (or the last line of a
  streamed answer) removed; every denial in a check answer turned into an allow.

Only the standard library is used. The proxy prints one line per mode change.
"""

from __future__ import annotations

import argparse
import contextlib
import http.client
import json
import select
import socket
import struct
import sys
import threading
import time
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

HTTP_MODES = (
    "pass",
    "refuse",
    "blackhole",
    "slow",
    "http500",
    "http503",
    "truncate",
    "empty",
    "garbage-json",
    "type-flip",
    "drop-last",
    "allow-all",
)
TCP_MODES = ("pass", "refuse", "blackhole", "slow")
HOP = {"connection", "keep-alive", "proxy-connection", "transfer-encoding", "te", "trailer", "upgrade", "content-length"}
# Decision enums of the engines: a type flip turns them into a value no adapter knows.
ENUM_PREFIXES = ("PERMISSIONSHIP_", "LOOKUP_PERMISSIONSHIP_", "EFFECT_", "KIND_")
ALLOW = {
    "PERMISSIONSHIP_NO_PERMISSION": "PERMISSIONSHIP_HAS_PERMISSION",
    "EFFECT_DENY": "EFFECT_ALLOW",
}
LIST_KEYS = ("objects", "pairs", "results", "result")


def _address(text: str) -> tuple[str, int]:
    host, _, port = text.rpartition(":")
    return host or "127.0.0.1", int(port)


def _abort(sock: socket.socket) -> None:
    """Close with a reset, so the peer sees the connection fail at once."""
    with contextlib.suppress(OSError):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    with contextlib.suppress(OSError):
        sock.close()


# ---- answer mutations -----------------------------------------------------------------------------


def _flip(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str) and value.startswith(ENUM_PREFIXES):
        return "X_UNKNOWN_VALUE"
    if isinstance(value, list):
        return [_flip(v) for v in value]
    if isinstance(value, dict):
        return {k: _flip(v) for k, v in value.items()}
    return value


def _allow(value: Any) -> Any:
    if value is False:
        return True
    if isinstance(value, str) and value in ALLOW:
        return ALLOW[value]
    if isinstance(value, list):
        return [_allow(v) for v in value]
    if isinstance(value, dict):
        return {k: _allow(v) for k, v in value.items()}
    return value


def _drop_last(document: Any) -> Any:
    if not isinstance(document, dict):
        return document
    for key in LIST_KEYS:
        value = document.get(key)
        if isinstance(value, list) and value:
            document[key] = value[:-1]
            return document
        if key == "result" and isinstance(value, dict) and value and all(isinstance(v, dict) for v in value.values()):
            # OpenFGA batch-check: {"result": {"<correlation id>": {"allowed": ...}}}
            last = sorted(value)[-1]
            document[key] = {k: v for k, v in value.items() if k != last}
            return document
    return document


def _lines(body: bytes) -> list[bytes] | None:
    """The lines of a newline-delimited JSON answer (a streamed answer), or None for one document."""
    parts = [line for line in body.splitlines() if line.strip()]
    if len(parts) < 2:
        return None
    try:
        for line in parts:
            json.loads(line)
    except ValueError:
        return None
    return parts


def mutate(mode: str, body: bytes) -> bytes:
    if mode == "truncate":
        return body[: len(body) // 2]
    if mode == "empty":
        return b""
    if mode == "garbage-json":
        return b'{"unexpected": true}'
    if mode not in ("type-flip", "drop-last", "allow-all"):
        return body
    lines = _lines(body)
    if lines is not None:
        if mode == "drop-last":
            return b"\n".join(lines[:-1]) + b"\n"
        change: Callable[[Any], Any] = _flip if mode == "type-flip" else _allow
        return b"\n".join(json.dumps(change(json.loads(line))).encode() for line in lines) + b"\n"
    try:
        document = json.loads(body)
    except ValueError:
        return body
    if mode == "type-flip":
        document = _flip(document)
    elif mode == "allow-all":
        document = _allow(document)
    else:
        document = _drop_last(document)
    return json.dumps(document).encode()


# ---- the proxy -----------------------------------------------------------------------------------


class Proxy:
    def __init__(self, kind: str, listen: tuple[str, int], upstream: tuple[str, int]) -> None:
        self.kind = kind
        self.listen = listen
        self.upstream = upstream
        self.mode = "pass"
        self.delay = 0.0
        self.version = 0  # bumped on every mode change, so held connections notice
        self.lock = threading.Lock()
        self.connections: set[socket.socket] = set()
        self.listener: socket.socket | None = None

    # -- listening

    def open(self) -> None:
        for attempt in range(50):  # the port can take a moment to be free again
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(self.listen)
            except OSError:
                sock.close()
                if attempt == 49:
                    raise
                time.sleep(0.1)
                continue
            break
        sock.listen(256)
        self.listener = sock
        threading.Thread(target=self._accept, args=(sock,), daemon=True).start()

    def close(self) -> None:
        listener, self.listener = self.listener, None
        if listener is not None:
            # On Linux, close() alone leaves a thread blocked in accept() holding the socket, which
            # keeps accepting; shutdown() wakes it and takes the socket out of the listening state.
            with contextlib.suppress(OSError):
                listener.shutdown(socket.SHUT_RDWR)
            with contextlib.suppress(OSError):
                listener.close()
        self.drop_connections()

    def drop_connections(self) -> None:
        with self.lock:
            held, self.connections = list(self.connections), set()
        for sock in held:
            _abort(sock)

    def _accept(self, listener: socket.socket) -> None:
        while True:
            try:
                conn, _ = listener.accept()
            except OSError:
                return  # the listener was closed
            with self.lock:
                self.connections.add(conn)
            target = self._serve_http if self.kind == "http" else self._serve_tcp
            threading.Thread(target=target, args=(conn,), daemon=True).start()

    def _forget(self, sock: socket.socket) -> None:
        with self.lock:
            self.connections.discard(sock)
        with contextlib.suppress(OSError):
            sock.close()

    def set_mode(self, mode: str, delay_ms: float) -> None:
        allowed = HTTP_MODES if self.kind == "http" else TCP_MODES
        if mode not in allowed:
            raise ValueError(f"unknown mode {mode!r} for a {self.kind} proxy")
        with self.lock:
            old = self.mode
            self.mode, self.delay = mode, max(0.0, delay_ms) / 1000.0
            self.version += 1
        if mode == "refuse" and old != "refuse":
            self.close()
        elif old == "refuse" and mode != "refuse":
            self.open()
        elif old == "blackhole" and mode != "blackhole":
            self.drop_connections()  # release what the blackhole held
        print(f"{time.time():.3f} mode {old} -> {mode} ({delay_ms} ms)", flush=True)

    def _hold(self, version: int) -> None:
        """Wait while the blackhole lasts (until the mode changes)."""
        while True:
            with self.lock:
                if self.version != version:
                    return
            time.sleep(0.05)

    # -- http

    def _serve_http(self, conn: socket.socket) -> None:
        rfile = conn.makefile("rb")
        upstream: http.client.HTTPConnection | None = None
        try:
            while True:
                line = rfile.readline(65537)
                if not line:
                    return
                parts = line.decode("latin-1").split()
                if len(parts) != 3:
                    return
                method, target, _ = parts
                headers: list[tuple[str, str]] = []
                length, chunked = 0, False
                while True:
                    raw = rfile.readline(65537)
                    if raw in (b"\r\n", b"\n", b""):
                        break
                    name, _, value = raw.decode("latin-1").partition(":")
                    name, value = name.strip(), value.strip()
                    headers.append((name, value))
                    if name.lower() == "content-length":
                        length = int(value)
                    elif name.lower() == "transfer-encoding" and "chunked" in value.lower():
                        chunked = True
                body = self._read_chunked(rfile) if chunked else (rfile.read(length) if length else b"")
                with self.lock:
                    mode, delay, version = self.mode, self.delay, self.version
                if mode == "blackhole":
                    self._hold(version)
                    return
                if mode == "slow" and delay:
                    time.sleep(delay)
                if mode in ("http500", "http503"):
                    status = 500 if mode == "http500" else 503
                    self._respond(conn, status, "Injected", [("Content-Type", "application/json")], b'{"error":"injected"}')
                    continue
                try:
                    if upstream is None:
                        upstream = http.client.HTTPConnection(*self.upstream, timeout=120)
                    forward = [(k, v) for k, v in headers if k.lower() not in HOP and k.lower() != "host"]
                    upstream.request(method, target, body=body, headers=dict(forward))
                    response = upstream.getresponse()
                    answer = response.read()
                    status, reason = response.status, response.reason
                    kept = [(k, v) for k, v in response.getheaders() if k.lower() not in HOP]
                    if response.will_close:
                        upstream.close()
                        upstream = None
                except (OSError, http.client.HTTPException):
                    if upstream is not None:
                        upstream.close()
                        upstream = None
                    self._respond(conn, 502, "Bad Gateway", [], b"")
                    continue
                if status == 200:
                    answer = mutate(mode, answer)
                self._respond(conn, status, reason, kept, answer)
        except OSError:
            return
        finally:
            if upstream is not None:
                upstream.close()
            with contextlib.suppress(OSError):
                rfile.close()
            self._forget(conn)

    @staticmethod
    def _read_chunked(rfile: Any) -> bytes:
        out = bytearray()
        while True:
            size_line = rfile.readline(65537)
            size = int(size_line.split(b";", 1)[0].strip() or b"0", 16)
            if size == 0:
                while rfile.readline(65537) not in (b"\r\n", b"\n", b""):
                    pass  # trailers
                return bytes(out)
            out += rfile.read(size)
            rfile.readline(65537)  # the CRLF after the chunk

    @staticmethod
    def _respond(conn: socket.socket, status: int, reason: str, headers: list[tuple[str, str]], body: bytes) -> None:
        head = [f"HTTP/1.1 {status} {reason or 'Status'}"]
        head += [f"{k}: {v}" for k, v in headers]
        head += [f"Content-Length: {len(body)}", "Connection: keep-alive", "", ""]
        conn.sendall("\r\n".join(head).encode("latin-1") + body)

    # -- tcp

    def _serve_tcp(self, conn: socket.socket) -> None:
        try:
            upstream = socket.create_connection(self.upstream, timeout=10)
        except OSError:
            self._forget(conn)
            return
        upstream.settimeout(None)
        with self.lock:
            self.connections.add(upstream)
        done = threading.Event()
        threading.Thread(target=self._pump, args=(conn, upstream, False, done), daemon=True).start()
        self._pump(upstream, conn, True, done)
        self._forget(conn)
        self._forget(upstream)

    def _pump(self, source: socket.socket, sink: socket.socket, answers: bool, done: threading.Event) -> None:
        """Copy bytes from source to sink until either side closes. `answers`: source is the server."""
        try:
            while not done.is_set():
                with self.lock:
                    mode, delay = self.mode, self.delay
                if mode == "blackhole":
                    time.sleep(0.05)
                    continue
                ready, _, _ = select.select([source], [], [], 0.2)
                if not ready:
                    continue
                data = source.recv(65536)
                if not data:
                    return
                if answers and mode == "slow" and delay:
                    time.sleep(delay)
                sink.sendall(data)
        except (OSError, ValueError):
            return
        finally:
            done.set()


class Admin(BaseHTTPRequestHandler):
    proxy: Proxy

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - the base class's name
        return

    def _send(self, status: int, payload: Any) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - the base class's name
        if self.path == "/health":
            self._send(200, {"ok": True})
        else:
            self._send(200, {"mode": self.proxy.mode, "delay_ms": self.proxy.delay * 1000})

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        try:
            request = json.loads(self.rfile.read(length) or b"{}")
            self.proxy.set_mode(str(request.get("mode", "pass")), float(request.get("delay_ms", 0)))
        except (ValueError, OSError) as error:
            self._send(400, {"error": str(error)})
            return
        self._send(200, {"mode": self.proxy.mode})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--kind", choices=("http", "tcp"), required=True)
    parser.add_argument("--listen", required=True)
    parser.add_argument("--upstream", required=True)
    parser.add_argument("--admin", required=True)
    args = parser.parse_args(argv)
    proxy = Proxy(args.kind, _address(args.listen), _address(args.upstream))
    proxy.open()
    Admin.proxy = proxy
    server = ThreadingHTTPServer(_address(args.admin), Admin)
    server.daemon_threads = True
    print(f"proxy {args.kind} {args.listen} -> {args.upstream}, admin {args.admin}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
