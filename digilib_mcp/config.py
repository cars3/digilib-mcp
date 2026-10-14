"""Central configuration for the DigiLIB MCP server.

Everything is settable through environment variables so the server can be
dropped into any deployment without code changes. A repo-local .env file
(gitignored) is auto-loaded if present, so settings don't have to be passed
in via the shell or the MCP client config.

Every setting is optional: with no configuration at all, all six data
sources work keyless.
"""

import os
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    """Load a .env file into os.environ. Existing env vars win (setdefault),
    so real environment settings always override the file."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


# Load .env before reading any config. Checks the digilib_mcp/ folder first
# (where users often place it) then the repo root. First value wins.
_here = Path(__file__).resolve().parent
_load_dotenv(_here / ".env")
_load_dotenv(_here.parent / ".env")

# Transport: "stdio" (default; desktop clients and CLI agents) or
# "streamable-http" (HTTP gateway for remote agents, e.g. Railway/Render/Fly).
TRANSPORT = os.environ.get("DIGILIB_TRANSPORT", "stdio")

# Optional polite-pool contact for OpenAlex. Unset by default; set it to
# your email to get more reliable service from OpenAlex.
OPENALEX_EMAIL = os.environ.get("DIGILIB_OPENALEX_EMAIL", "")

# Shared HTTP timeout for all source APIs, in seconds.
HTTP_TIMEOUT = 15.0

# Optional Google Books API key. Without it, basic search works but the
# shared anonymous quota is small; set this for reliable results.
GOOGLE_BOOKS_API_KEY = os.environ.get("DIGILIB_GOOGLE_BOOKS_API_KEY", "")
