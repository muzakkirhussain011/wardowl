"""What experiments X2 and X5 share: files, the two corpora, the oracle, the metrics and the sweep.

x2x5_prepare.py writes one folder per corpus (E: the enterprise scenario; M: MS MARCO with the
synthetic permission layouts of PREREG_X2_X5.md). x2_frontiers.py and x5_mitigation.py load a
folder with `load_corpus`, which checks every file's SHA-256 first. Every hit a store returns is
checked against an oracle that never calls wardowl (E: the scenario's `readable` and canary
detector; M: the subject's grant evaluated on the row's layout arrays) and scored against the exact
baseline the folder holds. Nothing here starts a store.
"""

from __future__ import annotations

import contextlib
import csv
import gzip
import hashlib
import json
import math
import os
import platform
import sys
import time
from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SEED = 20261029  # query pool, tenant field, subjects, round-robin order, bootstrap
TIE = 1e-4  # tie tolerance of permission-recall (background.tex)
LEVELS = (0.0006, 0.005, 0.02, 0.1, 0.3, 1.0)  # nominal selectivity levels of M
LEVEL_NAMES = ("0.06%", "0.5%", "2%", "10%", "30%", "100%")
FAMILIES = ("u", "c")  # uncorrelated (random groups), clustered (k-means groups)
SHAPES = ("groups", "tenant")
AXIS_K = 10  # K of HCBGen's over-fetch estimate, and the depth of the exact baseline
GLS_M = 2048  # |N_q| of Global-Local Selectivity, as Amanbayev et al. used it
LOCAL_MS = (100, 1000)  # local selectivity rho_m
WARMUP = 20  # untimed retrievals before a setting's passes
PASS1_SHARE = 0.4  # share of a setting's budget pass 1 may use; passes 2 and 3 repeat its list
E_NAME, M_NAME = "e", "m"
KB_PREFIX = "kb/"


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


# ---- files -----------------------------------------------------------------------------------------


def sha256_file(path: Path, block: int = 1 << 22) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(block), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, data: Any) -> None:
    """JSON written under a temporary name and renamed into place."""
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.parent / f"{path.name}.partial"
    partial.write_text(json.dumps(data, indent=1, default=str, allow_nan=True) + "\n", encoding="utf-8")
    partial.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl_gz(path: Path, records: Iterable[dict[str, Any]]) -> int:
    """One JSON object per line, gzip-compressed, written under a temporary name and renamed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.parent / f"{path.name}.partial"
    count = 0
    with gzip.open(partial, "wt", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, default=_plain, allow_nan=True) + "\n")
            count += 1
    partial.replace(path)
    return count


def read_jsonl_gz(path: Path) -> Iterator[Any]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _plain(value: Any) -> Any:
    """NumPy scalars and arrays as plain JSON values."""
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return str(value)


def write_checksums(folder: Path) -> dict[str, str]:
    """SHA-256 of every file in `folder` (not in subfolders), as checksums.json."""
    sums = {p.name: sha256_file(p) for p in sorted(folder.iterdir()) if p.is_file() and p.name != "checksums.json"}
    write_json(folder / "checksums.json", sums)
    return sums


def verify_checksums(folder: Path) -> dict[str, str]:
    """Raises when a file listed in checksums.json is missing or differs; returns the sums."""
    sums: dict[str, str] = read_json(folder / "checksums.json")
    bad = []
    for name, want in sums.items():
        path = folder / name
        if not path.is_file():
            bad.append(f"{name} is missing")
        elif sha256_file(path) != want:
            bad.append(f"{name} has another SHA-256")
    if bad:
        raise RuntimeError(f"{folder}: the data files do not match checksums.json: {bad}")
    log(f"{folder}: {len(sums)} files match checksums.json")
    return sums


# ---- environment -----------------------------------------------------------------------------------


def environment(packages: Sequence[str] = ()) -> dict[str, Any]:
    from importlib import metadata

    env: dict[str, Any] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpus": os.cpu_count(),
        "runner": os.environ.get("RUNNER_NAME"),
        "run": os.environ.get("GITHUB_RUN_ID"),
        "job": os.environ.get("GITHUB_JOB"),
        "sha": os.environ.get("GITHUB_SHA"),
    }
    with contextlib.suppress(OSError, ValueError):
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                env["memory_gib"] = round(int(line.split()[1]) / 2**20, 1)
    with contextlib.suppress(OSError, ValueError):
        model = [ln for ln in Path("/proc/cpuinfo").read_text().splitlines() if ln.startswith("model name")]
        env["cpu_model"] = model[0].split(":", 1)[1].strip() if model else None
    for name in ("wardowl", "numpy", *packages):
        try:
            env[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            env[name] = None
    with contextlib.suppress(ImportError):
        import wardowl

        env["wardowl_path"] = str(Path(wardowl.__file__).resolve().parent)
    return env


def scenario(repo: Path = REPO) -> Any:
    """acceptance/kaggle/enterprise_rag.py of this checkout, imported as a module (as X1 does)."""
    folder = repo / "acceptance" / "kaggle"
    if not (folder / "enterprise_rag.py").is_file():
        raise FileNotFoundError(f"{folder / 'enterprise_rag.py'} is missing: is {repo} the wardowl repository?")
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
    import enterprise_rag

    return enterprise_rag


def persona_type(persona: Any) -> str:
    """judy (only `board`), kb-reader (reads the FiQA base), no-groups (mallory), probe-<group>, other."""
    if "-probe-" in persona.id:
        return f"probe-{persona.groups[0]}"
    groups = set(persona.groups)
    if not groups:
        return "no-groups"
    if groups == {"board"}:
        return "judy"
    if groups & {"employees", "contractors"}:
        return "kb-reader"
    return "other"


# ---- the exact baseline and the measured axes (used by x2x5_prepare.py) ---------------------------


def expected_max_of_random(sorted_desc: np.ndarray, n: int, r: int) -> float:
    """E[max similarity over a uniformly random r-subset of n chunks], given the top similarities of
    all n in descending order (enough of them that the best of a random subset is almost surely
    among them). P(best rank > t) = C(n - t, r) / C(n, r), whose ratio from t - 1 to t is
    (n - t - r + 1) / (n - t + 1)."""
    j = len(sorted_desc)
    t = np.arange(1, j + 1, dtype=np.float64)
    num = n - t - r + 1
    den = n - t + 1
    logs = np.where(num > 0, np.log(np.maximum(num, 1e-300) / den), -np.inf)
    beyond = np.concatenate(([1.0], np.exp(np.cumsum(logs))))  # P(rank > t), t = 0..j
    at = beyond[:-1] - beyond[1:]  # P(rank = t), t = 1..j
    values = np.asarray(sorted_desc, dtype=np.float64)
    return float(np.dot(at, values) + beyond[-1] * values[-1])


def pair_truth(sims: np.ndarray, mask: np.ndarray) -> dict[str, Any]:
    """The exact top AXIS_K readable chunks of one query and the measured axes of PREREG section 3.

    `sims` holds the query's cosine similarity to every chunk (unit vectors), `mask` what the
    subject may read. Ranks count chunks strictly more similar, plus one.
    """
    n = int(sims.shape[0])
    readable = np.flatnonzero(mask)
    r = int(readable.shape[0])
    out: dict[str, Any] = {"R": r, "sigma": r / n}
    if r == 0:
        nan = math.nan
        out.update(top_rows=[], top_scores=[], acorn=nan, gls=nan, alpha=nan, rho100=nan, rho1000=nan)
        out.update(r1=None, r10=None)
        return out
    rs = sims[readable]
    kk = min(AXIS_K, r)
    part = np.argpartition(-rs, kk - 1)[:kk] if r > kk else np.arange(r)
    rows, scores = readable[part], rs[part]
    order = np.lexsort((rows, -scores))  # best first, ties by row
    rows, scores = rows[order], scores[order].astype(np.float64)
    best, kth = float(scores[0]), float(scores[kk - 1])
    depth = min(n, max(GLS_M, int(math.ceil(25.0 * n / r)) + 10))
    top = np.argpartition(-sims, depth - 1)[:depth] if depth < n else np.arange(n)
    top = top[np.argsort(-sims[top], kind="stable")]
    ranked = sims[top].astype(np.float64)
    local = {m: float(mask[top[: min(m, n)]].mean()) for m in LOCAL_MS}
    sigma_l = float(mask[top[: min(GLS_M, n)]].mean())
    ratio = sigma_l / out["sigma"]
    d_all = 1.0 - float(ranked[min(AXIS_K, n) - 1])
    out.update(
        top_rows=[int(x) for x in rows],
        top_scores=[float(x) for x in scores],
        acorn=best - expected_max_of_random(ranked, n, r),
        gls=(ratio - 1.0) / (ratio + 1.0),
        alpha=(n / r) * ((1.0 - kth) / max(d_all, 1e-6)) * AXIS_K,
        rho100=local[100],
        rho1000=local[1000],
        r1=1 + int(np.count_nonzero(sims > best)),
        r10=1 + int(np.count_nonzero(sims > float(scores[9]))) if r >= 10 else None,
    )
    return out


# ---- pairs and corpora --------------------------------------------------------------------------------

PAIR_COLUMNS = (
    "pid", "sid", "q", "order", "R", "sigma", "acorn", "gls", "alpha", "rho100", "rho1000", "r1", "r10",
    "top_rows", "top_scores",
)  # fmt: skip


@dataclass
class Pair:
    """One question asked by one subject, with the exact answer over what the subject may read."""

    pid: int
    sid: str
    q: int  # row of its vector in query_vectors.npy
    order: int  # position in the fixed round-robin order (PREREG section 4)
    R: int
    top_rows: list[int]
    top_scores: list[float]
    shape: str = ""  # M: groups or tenant
    original: bool = True  # E: one of the scenario run's 1,105 questions


def write_pairs(path: Path, rows: Sequence[dict[str, Any]], extra: Sequence[str]) -> None:
    columns = [*PAIR_COLUMNS, *extra]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            record = dict(row)
            record["top_rows"] = "|".join(str(x) for x in row.get("top_rows", []))
            record["top_scores"] = "|".join(f"{x:.7f}" for x in row.get("top_scores", []))
            writer.writerow(record)


def read_pairs(path: Path) -> list[Pair]:
    pairs = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            pairs.append(
                Pair(
                    pid=int(row["pid"]),
                    sid=row["sid"],
                    q=int(row["q"]),
                    order=int(row["order"]),
                    R=int(row["R"]),
                    top_rows=[int(x) for x in row["top_rows"].split("|") if x],
                    top_scores=[float(x) for x in row["top_scores"].split("|") if x],
                    shape=row.get("shape", "") or "",
                    original=row.get("original", "1") not in ("0", "False", "false"),
                )
            )
    pairs.sort(key=lambda p: p.order)
    return pairs


class Corpus:
    """A prepared corpus: vectors, ids, metadata for loading, subjects, pairs and the oracle."""

    name: str
    dim: int
    ids: list[str]
    row_of: dict[str, int]
    vectors: np.ndarray
    qvecs: np.ndarray
    pairs: list[Pair]
    authorizer: Any
    keyword_fields: tuple[str, ...]  # Qdrant's keyword indexes, as the original layout makes them
    tenant_field = "tenant"
    queries: dict[int, Any]

    def __len__(self) -> int:
        return len(self.ids)

    def subject(self, sid: str) -> Any:
        raise NotImplementedError

    def readable(self, sid: str, row: int) -> bool:
        raise NotImplementedError

    def leaks(self, sid: str, text: str) -> list[str]:
        return []

    def text(self, row: int) -> str:
        raise NotImplementedError

    def metadata(self, row: int) -> dict[str, Any]:
        raise NotImplementedError

    def documents(self, start: int, end: int) -> list[Any]:
        from wardowl import Document

        return [Document(self.ids[r], self.text(r), self.metadata(r)) for r in range(start, end)]

    def query(self, pair: Pair) -> Any:
        """The pair's query as a wardowl Query carrying its vector (made once per query row)."""
        found = self.queries.get(pair.q)
        if found is None:
            from wardowl import Query

            found = self.queries[pair.q] = Query(vector=self.qvecs[pair.q])
        return found

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "chunks": len(self.ids), "dim": self.dim, "pairs": len(self.pairs)}

    def _queries(self) -> None:
        self.queries = {}


class EnterpriseCorpus(Corpus):
    """E: the scenario's documents, people and questions, as x2x5_prepare.py saved them."""

    def __init__(self, folder: Path) -> None:
        er = scenario()
        self.er = er
        self.name = E_NAME
        self.docs = []
        for record in read_jsonl_gz(folder / "docs.jsonl.gz"):
            record["tenants"] = tuple(record["tenants"])
            record["readers"] = tuple(record["readers"])
            self.docs.append(er.Doc(**record))
        self.ids = [d.id for d in self.docs]
        self.row_of = {d.id: r for r, d in enumerate(self.docs)}
        self.people = {
            p["id"]: er.Persona(p["id"], p["tenant"], tuple(p["groups"]), p["role"])
            for p in read_json(folder / "people.json")
        }
        self.detector = er.LeakDetector(self.docs)
        self.authorizer = er.tenant_acl()
        self.vectors = np.load(folder / "vectors.npy", mmap_mode="r")
        self.dim = int(self.vectors.shape[1])
        self.qvecs = np.load(folder / "query_vectors.npy")
        self.pairs = read_pairs(folder / "pairs.csv")
        self.keyword_fields = ("allowed_users", "allowed_groups", "tenant")
        self.masks = self._masks()
        self._queries()

    def _masks(self) -> dict[str, np.ndarray]:
        """What each person may read, by the scenario's oracle, as enterprise_rag.Run._masks does it:
        chunks with the same tenants and readers share one decision."""
        groups: dict[tuple[Any, Any], int] = {}
        examples: list[Any] = []
        of_row = np.empty(len(self.docs), dtype=np.int32)
        for row, d in enumerate(self.docs):
            key = (d.tenants, d.readers)
            if key not in groups:
                groups[key] = len(examples)
                examples.append(d)
            of_row[row] = groups[key]
        masks = {}
        for pid, persona in self.people.items():
            decisions = np.array([self.er.readable(persona, d) for d in examples], dtype=bool)
            masks[pid] = decisions[of_row]
        return masks

    def subject(self, sid: str) -> Any:
        return self.er.person_subject(self.people[sid])

    def readable(self, sid: str, row: int) -> bool:
        return bool(self.masks[sid][row])

    def leaks(self, sid: str, text: str) -> list[str]:
        return self.detector.leaks(self.people[sid], text)

    def text(self, row: int) -> str:
        return self.docs[row].text

    def metadata(self, row: int) -> dict[str, Any]:
        return self.docs[row].metadata()


@dataclass
class Grant:
    """An M subject: the layout it reads, its granted divisions, departments and teams, its tenant."""

    sid: str
    family: str
    seed: int
    level: int
    shape: str
    tenant: str | None
    divs: frozenset[int]
    depts: frozenset[int]
    teams: frozenset[int]
    R: int = 0
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def field_name(self) -> str:
        return f"{self.family}{self.seed}"

    def tags(self) -> list[str]:
        return sorted(
            [f"v{d}" for d in self.divs] + [f"d{d}" for d in self.depts] + [f"t{t}" for t in self.teams]
        )

    def filter(self) -> Any:
        from wardowl.filters import And, In

        groups = In(self.field_name, self.tags())
        return groups if self.tenant is None else And(In("tenant", [self.tenant]), groups)

    def record(self) -> dict[str, Any]:
        return {
            "sid": self.sid,
            "family": self.family,
            "seed": self.seed,
            "level": self.level,
            "shape": self.shape,
            "tenant": self.tenant,
            "divs": sorted(self.divs),
            "depts": sorted(self.depts),
            "teams": sorted(self.teams),
            "R": self.R,
            **self.extra,
        }

    @classmethod
    def of(cls, record: dict[str, Any]) -> Grant:
        known = {"sid", "family", "seed", "level", "shape", "tenant", "divs", "depts", "teams", "R"}
        return cls(
            sid=record["sid"],
            family=record["family"],
            seed=int(record["seed"]),
            level=int(record["level"]),
            shape=record["shape"],
            tenant=record["tenant"],
            divs=frozenset(int(x) for x in record["divs"]),
            depts=frozenset(int(x) for x in record["depts"]),
            teams=frozenset(int(x) for x in record["teams"]),
            R=int(record.get("R", 0)),
            extra={k: v for k, v in record.items() if k not in known},
        )


class GrantAuthorizer:
    """The policy of M: a subject reads the chunks its grant (and tenant) admits.

    `filter_for` returns the grant as a wardowl filter; `check` evaluates that filter on each hit's
    metadata with wardowl's reference semantics. The harness's own oracle (`MsMarcoCorpus.readable`)
    checks every hit again on the layout arrays, without wardowl.
    """

    def __init__(self, grants: dict[str, Grant]) -> None:
        self.filters = {sid: g.filter() for sid, g in grants.items()}

    def filter_for(self, subject: Any, action: str = "read") -> Any:
        return self.filters[subject.id]

    def check(self, subject: Any, hits: Sequence[Any], action: str = "read") -> list[bool]:
        from wardowl.filters import matches

        f = self.filters[subject.id]
        return [matches(f, h.metadata) for h in hits]


def layout_tags(div: int, dept: int, team: int) -> list[str]:
    return [f"v{div}", f"d{dept}", f"t{team}"]


class MsMarcoCorpus(Corpus):
    """M: MS MARCO passages with ten permission layouts and a tenant field on every row."""

    def __init__(self, folder: Path) -> None:
        self.name = M_NAME
        self.ids, self.texts = [], []
        for doc_id, text in read_jsonl_gz(folder / "passages.jsonl.gz"):
            self.ids.append(doc_id)
            self.texts.append(text)
        self.row_of = {d: r for r, d in enumerate(self.ids)}
        if len(self.row_of) != len(self.ids):
            raise RuntimeError("M passage ids are not unique")
        layout = np.load(folder / "layout.npz")
        self.tenant = np.asarray(layout["tenant"])
        self.seeds = int(read_json(folder / "config.json")["seeds"])
        self.arrays: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
        for family in FAMILIES:
            for seed in range(self.seeds):
                key = f"{family}{seed}"
                self.arrays[key] = (
                    np.asarray(layout[f"{key}_div"]),
                    np.asarray(layout[f"{key}_dept"]),
                    np.asarray(layout[f"{key}_team"]),
                )
        self.grants = {r["sid"]: Grant.of(r) for r in read_json(folder / "subjects.json")}
        self.authorizer = GrantAuthorizer(self.grants)
        self.vectors = np.load(folder / "vectors.npy", mmap_mode="r")
        self.dim = int(self.vectors.shape[1])
        self.qvecs = np.load(folder / "query_vectors.npy")
        self.pairs = read_pairs(folder / "pairs.csv")
        self.keyword_fields = ("tenant", *self.arrays)
        self._subjects: dict[str, Any] = {}
        self._queries()

    def subject(self, sid: str) -> Any:
        if sid not in self._subjects:
            from wardowl import Subject

            self._subjects[sid] = Subject(sid)
        return self._subjects[sid]

    def readable(self, sid: str, row: int) -> bool:
        g = self.grants[sid]
        if g.tenant is not None and "ab"[int(self.tenant[row])] != g.tenant:
            return False
        div, dept, team = self.arrays[g.field_name]
        return int(div[row]) in g.divs or int(dept[row]) in g.depts or int(team[row]) in g.teams

    def text(self, row: int) -> str:
        return self.texts[row]

    def metadata(self, row: int) -> dict[str, Any]:
        record: dict[str, Any] = {"tenant": "ab"[int(self.tenant[row])]}
        for key, (div, dept, team) in self.arrays.items():
            record[key] = layout_tags(int(div[row]), int(dept[row]), int(team[row]))
        return record


def load_corpus(folder: Path, *, verify: bool = True) -> Corpus:
    if verify:
        verify_checksums(folder)
    kind = read_json(folder / "config.json")["corpus"]
    started = time.perf_counter()
    corpus: Corpus = EnterpriseCorpus(folder) if kind == E_NAME else MsMarcoCorpus(folder)
    log(f"corpus {kind}: {len(corpus):,} chunks, {len(corpus.pairs):,} pairs ({time.perf_counter() - started:.0f} s)")
    return corpus


# ---- one retrieval: safety and metrics -----------------------------------------------------------------


class LeakError(RuntimeError):
    """An unreadable hit, a canary of an unreadable document, or a wardowl violation."""

    def __init__(self, detail: dict[str, Any]) -> None:
        super().__init__(json.dumps(detail, default=str)[:2000])
        self.detail = detail


def check_safety(corpus: Corpus, pair: Pair, result: Any, label: str) -> None:
    problems = []
    if result.violations:
        problems.append(f"wardowl's re-check removed {result.violations} hits: the store ignored the filter")
    for hit in result.hits:
        row = corpus.row_of.get(hit.id)
        if row is None:
            problems.append(f"{hit.id} is not in the corpus")
        elif not corpus.readable(pair.sid, row):
            problems.append(f"{hit.id} is not readable by {pair.sid}")
        leaked = corpus.leaks(pair.sid, hit.text)
        if leaked:
            problems.append(f"{hit.id} holds canaries of {leaked}")
    if problems:
        raise LeakError({"setting": label, "pid": pair.pid, "subject": pair.sid, "problems": problems})


def score(corpus: Corpus, pair: Pair, hits: Sequence[Any], k: int) -> dict[str, Any]:
    """PREREG section 6's metrics of one retrieval at depth k, suffixed with k."""
    hits = list(hits)[:k]
    want = min(k, pair.R)
    query = corpus.qvecs[pair.q]
    floor = pair.top_scores[want - 1] - TIE if want else math.inf
    best = pair.top_scores[0] - TIE if want else math.inf
    exact_ids = {corpus.ids[r] for r in pair.top_rows[:want]}
    counting = id_hits = 0
    best_found = False
    sims = []
    for hit in hits:
        row = corpus.row_of.get(hit.id)
        if row is None:
            continue
        sim = float(np.dot(corpus.vectors[row], query))
        sims.append(sim)
        if corpus.readable(pair.sid, row):
            counting += sim >= floor
            best_found = best_found or sim >= best
        id_hits += hit.id in exact_ids
    n = len(hits)
    recall = min(counting, want) / want if want else None
    out: dict[str, Any] = {
        f"n{k}": n,
        f"recall{k}": recall,
        f"rid{k}": id_hits / want if want else None,  # id-based, as wardowl's sampled_recall counts
        f"max{k}": int(recall == 1.0) if want else int(n == 0),
        f"empty{k}": int(n == 0) if want else None,
        f"short{k}": int(n < want) if want else None,
        f"gross{k}": int(not best_found) if want else None,
        f"gap{k}": float(np.mean(pair.top_scores[:want]) - np.mean(sims)) if want and sims else None,
        f"hits{k}": "|".join(h.id for h in hits),
    }
    return out


def id_recall(corpus: Corpus, pair: Pair, hits: Sequence[Any], k: int) -> float | None:
    """Share of the exact top min(k, R) ids among the first k hits (no tie credit)."""
    want = min(k, pair.R)
    if not want:
        return None
    exact_ids = {corpus.ids[r] for r in pair.top_rows[:want]}
    return sum(h.id in exact_ids for h in list(hits)[:k]) / want


# ---- timing and the sweep ------------------------------------------------------------------------------


class Deadline:
    """The job's own end, before its runner's timeout: no setting starts after it."""

    def __init__(self, minutes: float) -> None:
        self.end = time.monotonic() + minutes * 60.0

    def left(self) -> float:
        return self.end - time.monotonic()

    def share(self, parts: int, reserve: float = 300.0) -> float:
        """A fair share of what is left, after `reserve` seconds for writing and stopping."""
        return max(0.0, (self.left() - reserve) / max(1, parts))


class LastEvent:
    """A wardowl observer that keeps the latest RetrievalEvent."""

    def __init__(self) -> None:
        self.event: Any = None

    def __call__(self, event: Any) -> None:
        self.event = event


@dataclass
class Sweep:
    """One setting's (or arm's) run over its pairs: rows per pair and what the run did."""

    rows: list[dict[str, Any]]
    info: dict[str, Any]


def event_fields(event: Any, k: int) -> dict[str, Any]:
    if event is None:
        return {}
    return {
        f"complete{k}": int(bool(event.complete)),
        f"shortfall{k}": event.shortfall,
        f"fallback{k}": event.fallback,
        f"sfms{k}": event.shortfall_ms,
        f"sampled{k}": event.sampled_recall,
        f"searches{k}": event.searches,
        f"storems{k}": event.search_ms,
    }


def sweep(
    corpus: Corpus,
    retriever: Any,
    timer: LastEvent,
    pairs: Sequence[Pair],
    *,
    label: str,
    budget: float,
    deadline: Deadline,
    ks: Sequence[int] = (10,),
    timed_k: int = 10,
    passes: int = 3,
    before_pass: Callable[[int], None] | None = None,
    plan: Callable[[Pair, int], str] | None = None,
    calls: Callable[[], list[Any]] | None = None,
) -> Sweep:
    """PREREG section 4's procedure for one setting: warm-up, pass 1 over a balanced prefix of
    `pairs` within 40% of `budget`, then passes 2 and 3 over the same prefix at `timed_k`.

    `plan` (pgvector) returns the plan kind of a first-pass search, outside its timing; `calls`
    (X5) returns what the backend was asked to do during the last retrieval; `before_pass` reseeds
    the recall monitor's sampler. Every hit of every pass is checked; a leak stops everything.
    """
    started = time.perf_counter()
    warm_errors = 0
    for pair in pairs[:WARMUP]:
        try:
            warm = retriever.retrieve(corpus.query(pair), corpus.subject(pair.sid), k=timed_k)
        except LeakError:
            raise
        except Exception as error:  # a failing store shows up in pass 1 too, with its message
            warm_errors += 1
            if warm_errors == 1:
                log(f"  {label}: warm-up error: {type(error).__name__}: {error}")
            continue
        check_safety(corpus, pair, warm, f"{label} warm-up")
    if calls is not None:
        calls()
    pass1_end = started + PASS1_SHARE * budget
    rows: dict[int, dict[str, Any]] = {}
    done: list[Pair] = []
    errors: dict[int, str] = {}
    samples = retrievals = 0
    cut = "none"
    if before_pass is not None:
        before_pass(0)
    for pair in pairs:
        if time.perf_counter() > pass1_end:
            cut = "budget"
            break
        if deadline.left() < 120:
            cut = "deadline"
            break
        row: dict[str, Any] = {"pid": pair.pid}
        try:
            for k in ks:
                clock = time.perf_counter()
                result = retriever.retrieve(corpus.query(pair), corpus.subject(pair.sid), k=k)
                ms = (time.perf_counter() - clock) * 1000.0
                event = timer.event
                retrievals += 1
                check_safety(corpus, pair, result, label)
                row.update(score(corpus, pair, result.hits, k))
                row.update(event_fields(event, k))
                row[f"complete{k}"] = int(bool(result.complete))
                if result.sampled_recall is not None:
                    samples += 1
                    found = id_recall(corpus, pair, result.hits, k)
                    row.setdefault("samples", []).append([0, k, result.sampled_recall, found])
                if calls is not None:
                    row[f"calls{k}"] = calls()
                if k == timed_k:
                    row["lat"] = [round(ms, 4)]
                    row["slat"] = [round(float(event.search_ms), 4) if event is not None else None]
                if plan is not None:
                    row[f"plan{k}"] = plan(pair, k)
        except LeakError:
            raise
        except Exception as error:
            errors[pair.pid] = f"{type(error).__name__}: {error}"
            if len(errors) <= 3:
                log(f"  {label}: error on pair {pair.pid}: {errors[pair.pid]}")
            if calls is not None:
                calls()
            continue
        rows[pair.pid] = row
        done.append(pair)
        if len(done) % 1000 == 0:
            log(f"  {label}: pass 1, {len(done)} of {len(pairs)} pairs ({time.perf_counter() - started:.0f} s)")
    pass1_seconds = time.perf_counter() - started
    finished_passes = 1
    later: dict[int, str] = {}
    for p in range(1, passes):
        if before_pass is not None:
            before_pass(p)
        complete_pass = True
        for pair in done:
            if deadline.left() < 120:
                complete_pass, cut = False, "deadline"
                break
            clock = time.perf_counter()
            try:
                result = retriever.retrieve(corpus.query(pair), corpus.subject(pair.sid), k=timed_k)
            except LeakError:
                raise
            except Exception as error:  # the pair keeps its pass-1 metrics, and one timing fewer
                later.setdefault(pair.pid, f"pass {p + 1}: {type(error).__name__}: {error}")
                continue
            ms = (time.perf_counter() - clock) * 1000.0
            event = timer.event
            retrievals += 1
            check_safety(corpus, pair, result, label)
            row = rows[pair.pid]
            row["lat"].append(round(ms, 4))
            row["slat"].append(round(float(event.search_ms), 4) if event is not None else None)
            if event is not None and event.shortfall is not None:
                row.setdefault("sfms_passes", []).append([p, event.shortfall_ms])
            if result.sampled_recall is not None:
                samples += 1
                row.setdefault("samples", []).append(
                    [p, timed_k, result.sampled_recall, id_recall(corpus, pair, result.hits, timed_k)]
                )
            if calls is not None:
                calls()
        if not complete_pass:
            break
        finished_passes += 1
    for pid, message in errors.items():
        rows.setdefault(pid, {"pid": pid})["err"] = message
    for pid, message in later.items():
        rows[pid]["err_later"] = message
    info = {
        "pairs_listed": len(pairs),
        "pairs_run": len(done),
        "cut": cut,
        "passes": finished_passes,
        "errors": len(errors),
        "error_examples": list(errors.values())[:5],
        "later_pass_errors": len(later),
        "later_error_examples": list(later.values())[:3],
        "warmup_errors": warm_errors,
        "retrievals": retrievals,
        "sampled": samples,
        "pass1_seconds": round(pass1_seconds, 1),
        "seconds": round(time.perf_counter() - started, 1),
        "budget_seconds": round(budget, 1),
    }
    if not done and errors:
        raise RuntimeError(f"{label}: every retrieval failed, e.g. {next(iter(errors.values()))}")
    log(
        f"  {label}: {len(done)} of {len(pairs)} pairs, {finished_passes} passes, {len(errors)} errors, "
        f"{info['seconds']:.0f} s (cut: {cut})"
    )
    return Sweep(list(rows.values()), info)


def summarize_rows(rows: Sequence[dict[str, Any]], k: int = 10) -> dict[str, Any]:
    """Mean recall, empty and short rates, and latency percentiles of one setting's rows."""
    recall = [r[f"recall{k}"] for r in rows if r.get(f"recall{k}") is not None]
    empty = [r[f"empty{k}"] for r in rows if r.get(f"empty{k}") is not None]
    short = [r[f"short{k}"] for r in rows if r.get(f"short{k}") is not None]
    lat = [float(np.median(r["lat"])) for r in rows if r.get("lat")]
    out: dict[str, Any] = {
        "pairs": len(rows),
        f"recall{k}": float(np.mean(recall)) if recall else None,
        f"err{k}": float(np.mean(empty)) if empty else None,
        f"short{k}": float(np.mean(short)) if short else None,
    }
    if lat:
        p50, p95, p99 = np.percentile(lat, [50, 95, 99])
        out.update(p50_ms=float(p50), p95_ms=float(p95), p99_ms=float(p99), qps=1000.0 / float(np.mean(lat)))
    return out


def markdown_table(header: Sequence[str], rows: Iterable[Sequence[Any]]) -> list[str]:
    def cell(value: Any) -> str:
        if value is None:
            return "n/a"
        if isinstance(value, float):
            if math.isnan(value):
                return "n/a"
            return f"{value:.3f}" if abs(value) < 10 else f"{value:.1f}"
        return str(value).replace("|", "/")

    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return [*lines, ""]
