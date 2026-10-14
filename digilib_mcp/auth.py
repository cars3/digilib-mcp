"""Shared-secret bearer-token gate for the streamable-http gateway.

A simple authorization layer for a single-user MCP gateway: it checks that
incoming HTTP requests carry `Authorization: Bearer <DIGILIB_GATEWAY_TOKEN>`
matching the secret in the DIGILIB_GATEWAY_TOKEN env var.

This is NOT OAuth 2.1. For multi-user / third-party client support, use the
MCP SDK's native auth instead:

    MCPServer(
        "digilib",
        settings=Settings(auth=AuthSettings(...)),
        token_verifier=YourTokenVerifier(),
    )

which auto-wires BearerAuthBackend + RequireAuthMiddleware and exposes the
OAuth 2.1 protected-resource metadata endpoints.
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class BearerTokenGate:
    """ASGI middleware: reject requests without a valid bearer token.

    The token is compared in constant-ish time to avoid trivial timing
    leaks, though for a single shared secret this is belt-and-braces.
    """

    def __init__(self, app: ASGIApp, token: str) -> None:
        self.app = app
        self.token = token

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Only gate HTTP; pass through lifespan/websocket scopes untouched.
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        header = request.headers.get("Authorization", "")
        if header.startswith("Bearer "):
            presented = header[len("Bearer "):].strip()
        else:
            presented = ""

        # Constant-time comparison.
        import hmac

        if presented and hmac.compare_digest(presented, self.token):
            await self.app(scope, receive, send)
            return

        response = JSONResponse(
            {"jsonrpc": "2.0", "error": {"code": -32001, "message": "Unauthorized: missing or invalid bearer token"}},
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )
        await response(scope, receive, send)