"""A RAG service on FastAPI: every search and every answer uses only chunks the caller may read.

    pip install wardowl fastapi uvicorn pyjwt
    export WARDOWL_DEMO_JWT_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
    uvicorn --factory rag_service:create_app --app-dir examples/fastapi_rag

How it holds:

1. Identity comes from a verified access token, never from the request. `caller()` checks the
   token's signature, issuer, audience and expiry, then builds the `Subject` from its claims: the
   user (`sub`), their groups (`groups`) and their tenant (`tid`).
2. The request body cannot name a user, a group or a tenant: unknown fields are refused with 422,
   and nothing reads the query string.
3. Retrieval runs through `PermissionedRetriever` with `AllOf(TenantAuthorizer(), ...)`, so a caller
   sees only their own tenant's chunks, and within it only those shared with them or their groups.
4. `/ask` hands the model only the chunks that passed the check.
5. A failed permission check answers 503 with no details; the details go to the server log.
6. Each retrieval is logged as a structured event (who asked, what came back), never the query or
   the text.
7. A request body over 256 KiB is refused with 413 before it is read in full, and so before the
   token is checked: FastAPI reads the whole body before it runs the dependency that checks it.

This is a reference, not a product. The documents are synthetic and kept in memory; the token is an
HS256 JWT signed with a secret from the environment; `cite_sources` stands in for your model. In
production, verify tokens from your identity provider with its published keys (RS256 or ES256),
use a real vector store and permission service, wrap the authorizer's cache to suit your revocation
needs (docs/revocation.md), and send the events to your audit pipeline.
"""

# No `from __future__ import annotations` here: FastAPI resolves string annotations against the module's
# globals, so `Annotated[Subject, Depends(caller)]`, with `caller` defined inside `create_app`, would
# silently become a required query parameter named `subject`.

import json
import logging
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from wardowl import (
    AllOf,
    AuthorizationError,
    CachingAuthorizer,
    Document,
    Hit,
    InMemoryBackend,
    MetadataACLAuthorizer,
    PermissionedRetriever,
    RetrievalEvent,
    RetrievalResult,
    SearchBackend,
    Subject,
    TenantAuthorizer,
)

log = logging.getLogger("rag_service")

Model = Callable[[str, Sequence[Hit]], str]
"""Your language model: the question and the permitted passages in, an answer out."""


@dataclass(frozen=True)
class Settings:
    """How tokens are verified, from the environment."""

    jwt_secret: str = field(repr=False)  # out of repr(), which logs, debuggers and error reporters use
    issuer: str = "https://id.example.test"
    audience: str = "rag-service"

    @classmethod
    def from_env(cls) -> "Settings":
        secret = os.environ.get("WARDOWL_DEMO_JWT_SECRET", "")
        if len(secret) < 32:
            raise RuntimeError("set WARDOWL_DEMO_JWT_SECRET to at least 32 random characters")
        return cls(
            secret,
            os.environ.get("WARDOWL_DEMO_ISSUER", cls.issuer),
            os.environ.get("WARDOWL_DEMO_AUDIENCE", cls.audience),
        )


def demo_documents() -> list[Document]:
    """Synthetic chunks for two tenants that use the same document names and groups."""
    documents = []
    for tenant in ("acme", "globex"):
        name = tenant.title()
        documents += [
            Document(
                f"{tenant}/handbook#1",
                f"{name} handbook: annual leave is 25 days.",
                {"tenant": tenant, "doc_id": f"{tenant}/handbook", "allowed_groups": ["*"]},
            ),
            Document(
                f"{tenant}/runbook#1",
                f"{name} engineering runbook: deploys go out on Tuesdays.",
                {"tenant": tenant, "doc_id": f"{tenant}/runbook", "allowed_groups": ["engineering"]},
            ),
            Document(
                f"{tenant}/salaries#1",
                f"{name} HR: the 2026 salary bands and leave payouts.",
                {"tenant": tenant, "doc_id": f"{tenant}/salaries", "allowed_groups": ["hr"]},
            ),
        ]
    return documents


def log_event(event: RetrievalEvent) -> None:
    """A structured audit line per retrieval: who asked and what came back, never the query or text."""
    log.info("retrieval %s", json.dumps(event.to_dict(), sort_keys=True))


def build_retriever(backend: SearchBackend) -> PermissionedRetriever:
    authorizer = CachingAuthorizer(AllOf(TenantAuthorizer(), MetadataACLAuthorizer()), ttl=30)
    return PermissionedRetriever(backend, authorizer, observers=[log_event])


def cite_sources(question: str, passages: Sequence[Hit]) -> str:
    """Stands in for your model. It is given the question and the permitted passages, nothing else."""
    if not passages:
        return "Nothing you have access to answers this."
    return " ".join(p.text for p in passages)


class BodyLimit:
    """Refuses a request body over `limit` bytes with 413, by its Content-Length and by the bytes
    received, before the application reads it, then hands the body on."""

    def __init__(self, app: ASGIApp, limit: int = 256 * 1024) -> None:
        self.app, self.limit = app, limit

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        too_large = JSONResponse({"detail": "the request body is too large"}, status_code=413)
        declared = dict(scope["headers"]).get(b"content-length", b"")
        if declared.isdigit() and (len(declared) > 18 or int(declared) > self.limit):
            await too_large(scope, receive, send)
            return
        body = bytearray()
        more = True
        while more:
            message = await receive()
            if message["type"] != "http.request":  # the client went away
                return
            body += message.get("body", b"")
            if len(body) > self.limit:
                await too_large(scope, receive, send)
                return
            more = bool(message.get("more_body", False))
        replayed = False

        async def replay() -> Message:
            nonlocal replayed
            if replayed:
                return await receive()
            replayed = True
            return {"type": "http.request", "body": bytes(body), "more_body": False}

        await self.app(scope, replay, send)


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")  # a body that names a user, group or tenant is refused

    query: str = Field(min_length=1, max_length=2000)
    k: int = Field(default=5, ge=1, le=20)


class Passage(BaseModel):
    id: str
    text: str
    score: float


class SearchResponse(BaseModel):
    passages: list[Passage]
    complete: bool


class AskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, max_length=2000)


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


def create_app(
    settings: Settings | None = None,
    retriever: PermissionedRetriever | None = None,
    model: Model = cite_sources,
) -> FastAPI:
    settings = settings or Settings.from_env()
    retriever = retriever or build_retriever(InMemoryBackend(demo_documents()))
    bearer = HTTPBearer(auto_error=False)
    app = FastAPI(title="Permission-aware RAG")
    app.add_middleware(BodyLimit)

    def caller(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> Subject:
        """The verified caller, from the token alone."""
        refused = HTTPException(401, "a valid bearer token is required", headers={"WWW-Authenticate": "Bearer"})
        if credentials is None:
            raise refused
        try:
            claims = jwt.decode(
                credentials.credentials,
                settings.jwt_secret,
                algorithms=["HS256"],  # never taken from the token's own header
                audience=settings.audience,
                issuer=settings.issuer,
                options={"require": ["exp", "iss", "aud", "sub", "tid"]},
            )
        except jwt.InvalidTokenError:
            raise refused from None
        user, groups, tenant = claims["sub"], claims.get("groups", []), claims["tid"]
        if not isinstance(user, str) or not user or not isinstance(tenant, str) or not tenant:
            raise refused
        if not isinstance(groups, list) or not all(isinstance(g, str) for g in groups):
            raise refused
        return Subject(user, groups, {"tenant": tenant})

    async def permitted(subject: Subject, query: str, k: int) -> RetrievalResult:
        try:
            return await retriever.aretrieve(query, subject, k)
        except AuthorizationError:
            log.exception("permission check failed; nothing was returned")  # for operators only
            raise HTTPException(503, "the permission check could not be completed, so nothing was returned") from None

    @app.post("/search")
    async def search(body: SearchRequest, subject: Annotated[Subject, Depends(caller)]) -> SearchResponse:
        result = await permitted(subject, body.query, body.k)
        passages = [Passage(id=h.id, text=h.text, score=h.score) for h in result.hits]
        return SearchResponse(passages=passages, complete=result.complete)

    @app.post("/ask")
    async def ask(body: AskRequest, subject: Annotated[Subject, Depends(caller)]) -> AskResponse:
        result = await permitted(subject, body.question, 5)
        # Only chunks that passed the permission check reach the model.
        return AskResponse(answer=model(body.question, result.hits), sources=[h.id for h in result.hits])

    return app
