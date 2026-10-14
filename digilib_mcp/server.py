"""DigiLIB MCP server entrypoint.

Exposes three tools (search_papers, search_books, export_research_tool),
one prompt (digilib_researcher - the DigiLIB persona system prompt), and
one resource (digilib://prompts/researcher) for clients that prefer
resources.

Run:
    digilib-mcp                                     # console script (stdio)
    python -m digilib_mcp.server                    # module form (stdio)
    DIGILIB_TRANSPORT=streamable-http python -m digilib_mcp.server
"""

import os
import sys
from pathlib import Path

# Allow `python -m digilib_mcp.server` AND `python digilib_mcp/server.py`
# by making the repo root importable.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from mcp.server.mcpserver import MCPServer

from digilib_mcp.config import TRANSPORT
from digilib_mcp.services.books import BookService
from digilib_mcp.services.papers import PaperService
from digilib_mcp.digiexport import export_research

mcp = MCPServer("digilib")

_PROMPT_PATH = Path(__file__).resolve().parent / "context" / "researcher.md"
_papers = PaperService()
_books = BookService()


# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------

@mcp.tool()
async def search_papers(
    keywords: list[str],
    year_from: int | None = None,
    year_to: int | None = None,
    size: int = 10,
) -> str:
    """Search academic literature across OpenAlex, arXiv, Semantic Scholar,
    and Crossref.

    Args:
        keywords:  key terms, e.g. ["transformer attention"]. Craft 2-5
                   focused queries (expand acronyms, add synonyms, use
                   technical phrasing) for the best coverage.
        year_from: restrict to papers from this year onwards. Applied by
                   OpenAlex and Crossref only.
        year_to:   restrict to papers up to this year. Applied by OpenAlex
                   and Crossref only.
        size:      results per source per keyword (default 10, max 40).

    Returns:
        A numbered plain-text list of deduplicated results with title, authors,
        year, source, link, and abstract per entry.
    """
    return await _papers.search(
        keywords, size=size, year_from=year_from, year_to=year_to
    )


@mcp.tool()
async def search_books(
    keywords: list[str],
    size: int = 10,
) -> str:
    """Search books across Open Library and Google Books.

    Args:
        keywords: key terms; broader, book-friendly phrasing works best.
        size:     results per source per keyword (default 10).

    Returns:
        A numbered plain-text list of deduplicated book results with title,
        authors, year, source, link, and description per entry.
    """
    return await _books.search(keywords, size=size)


@mcp.tool()
def export_research_tool(
    conversation_summary: str,
    literature_recommended: list[str],
    liked_articles: list[dict] | None = None,
    citation_formats: list[str] | None = None,
) -> str:
    """Build the LaTeX source for a research export (literature review +
    conversation summary + citations in APA/Chicago/MLA) and return it.

    This tool does NOT render a PDF - it returns the raw LaTeX document
    source. You, the assistant calling this tool, are responsible for
    rendering it yourself:
      1. Write the returned LaTeX to a `.tex` file (e.g. `digilib_export.tex`)
         in the user's project or Downloads folder.
      2. If `pdflatex` is available, compile it to PDF with
         `pdflatex -interaction=nonstopmode digilib_export.tex` and give the
         user the path to the resulting PDF.
      3. If `pdflatex` is NOT available, just save the `.tex` file and tell the
         user where it is and how to compile it (e.g. install TeX, or use an
         online LaTeX compiler such as Overleaf).
    Always save the `.tex` file regardless, so the user keeps the source.

    Args:
        conversation_summary:   plain-text summary of the conversation, written
                                by the calling LLM.
        literature_recommended: list of plain-text lines for the Literature
                                Review section (one bullet per line).
        liked_articles:         citation entries, each a dict with
                                title/authors/year/link keys.
        citation_formats:       subset of ["APA", "Chicago", "MLA"].

    Returns:
        The complete LaTeX document source as a string.
    """
    return export_research(
        conversation_summary=conversation_summary,
        literature_recommended=literature_recommended,
        liked_articles=liked_articles,
        citation_formats=citation_formats,
    )


# --------------------------------------------------------------------------
# Prompt + Resource: system-prompt delivery
# --------------------------------------------------------------------------

@mcp.prompt()
def digilib_researcher() -> str:
    """Return the DigiLIB researcher system prompt (persona/instructions)."""
    return _PROMPT_PATH.read_text(encoding="utf-8")


@mcp.resource("digilib://prompts/researcher")
def researcher_prompt_resource() -> str:
    """Raw contents of the DigiLIB researcher system prompt."""
    return _PROMPT_PATH.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> None:
    """Run the server. stdio by default; streamable-http via DIGILIB_TRANSPORT."""
    if TRANSPORT == "streamable-http":
        # Gateway mode: bind to all interfaces and honor the PORT env var
        # (Railway/Render/Fly inject it). We build the Starlette app directly
        # so we can attach auth middleware, then run uvicorn ourselves.
        import uvicorn
        from mcp.server.transport_security import TransportSecuritySettings

        _host = os.environ.get("DIGILIB_HOST", "0.0.0.0")
        _port = int(os.environ.get("PORT") or os.environ.get("DIGILIB_PORT", "8000"))
        _token = os.environ.get("DIGILIB_GATEWAY_TOKEN", "")
        _allowed_hosts = os.environ.get("DIGILIB_ALLOWED_HOSTS", "")

        # The MCP SDK's transport-security middleware validates the Host
        # header against an allow-list (default: localhost only) to prevent
        # DNS rebinding. Behind a reverse proxy (Railway/Render/Fly) the
        # incoming Host is the public domain, which won't match that default
        # and yields 421 "Invalid Host header". The proxy already handles
        # DNS rebinding at its edge, and our bearer gate is the real auth
        # layer, so we disable this check unless DIGILIB_ALLOWED_HOSTS is
        # set explicitly (comma-separated, e.g. "example.com,*.example.com").
        if _allowed_hosts:
            _ts = TransportSecuritySettings(
                allowed_hosts=[h.strip() for h in _allowed_hosts.split(",") if h.strip()]
            )
        else:
            _ts = TransportSecuritySettings(enable_dns_rebinding_protection=False)

        app = mcp.streamable_http_app(transport_security=_ts)
        if _token:
            from digilib_mcp.auth import BearerTokenGate

            app.add_middleware(BearerTokenGate, token=_token)
            print("[digilib] gateway auth enabled: bearer token required", flush=True)
        else:
            print(
                "[digilib] WARNING: DIGILIB_GATEWAY_TOKEN is not set - the "
                "gateway is UNAUTHENTICATED. Anyone with the URL can call the "
                "tools. Set DIGILIB_GATEWAY_TOKEN to lock it down.",
                flush=True,
            )
        uvicorn.run(app, host=_host, port=_port)
    else:
        mcp.run(transport=TRANSPORT)


if __name__ == "__main__":
    main()
