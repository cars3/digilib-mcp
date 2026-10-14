# digilib-mcp — Agent Guide

**DigiLIB stands for "digital librarian".** This repository is an MCP server
that gives the ability of a digital librarian to the agent of choice: search
academic papers and books across six free sources, and export a cited
literature review as LaTeX.

This file is the canonical instruction file for AI coding agents working in,
with, or on this repository. `CLAUDE.md`, `CODEX.md`, `OPENCODE.md`, and
`KIMI.md` simply import it. The canonical agent skill lives at
`.agents/skills/digilib/SKILL.md`.

## What this server provides

- `search_papers(keywords, year_from?, year_to?, size?)` — OpenAlex, arXiv, Semantic Scholar, Crossref
- `search_books(keywords, size?)` — Open Library, Google Books
- `export_research_tool(conversation_summary, literature_recommended, liked_articles?, citation_formats?)` — a complete LaTeX document
- `digilib_researcher` prompt and `digilib://prompts/researcher` resource — the DigiLIB persona

No API keys are required for any feature. All six sources are keyless.

## Run it

```bash
# Zero-install, stdio (most clients)
uvx --from git+https://github.com/cars3/digilib-mcp digilib-mcp

# From a checkout
python -m digilib_mcp.server                                        # stdio (default)
DIGILIB_TRANSPORT=streamable-http python -m digilib_mcp.server      # HTTP gateway
```

## Connect digilib to an agent

One-page registration guides for every supported agent: `docs/agents/`.

| Agent | Registration location | Guide |
|---|---|---|
| Claude Code | `.mcp.json` / `claude mcp add` | docs/agents/claude-code.md |
| Claude Desktop | `claude_desktop_config.json` | docs/agents/claude-desktop.md |
| Codex | `~/.codex/config.toml` | docs/agents/codex.md |
| Antigravity (CLI / IDE / 2.0) | `~/.gemini/config/mcp_config.json`, `.agents/mcp_config.json` | docs/agents/antigravity.md |
| Cursor | `.cursor/mcp.json` | docs/agents/cursor.md |
| OpenCode | `opencode.json(c)` | docs/agents/opencode.md |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | docs/agents/windsurf.md |
| Qwen Code | `~/.qwen/settings.json` | docs/agents/qwen.md |
| Kimi CLI | `~/.kimi/mcp.json` | docs/agents/kimi.md |
| Grok CLI | `~/.grok/config.toml` | docs/agents/grok.md |
| GitHub Copilot CLI | `~/.copilot/mcp-config.json` | docs/agents/copilot-cli.md |
| Pi | `~/.pi/agent/mcp.json` (`pi mcp add`) | docs/agents/pi.md |
| Hermes Agent | `~/.hermes/config.yaml` (`mcp_servers`) | docs/agents/hermes.md |
| Gemini CLI (legacy) | see guide | docs/agents/gemini-cli.md |
| Any other MCP client | standard stdio pattern | docs/agents/generic.md |

The universal stdio pattern most clients accept:

```json
{
  "mcpServers": {
    "digilib": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/cars3/digilib-mcp", "digilib-mcp"]
    }
  }
}
```

If you are an agent asked to connect digilib on a user's machine: read the
guide for the target agent, apply its snippet to the file it names (creating
the file if needed, preserving anything already there), and run the guide's
verification step.

## Using the tools well

- Craft 2-5 focused queries before calling `search_papers`: expand acronyms,
  add synonyms, prefer technical phrasing. Book queries take broader,
  book-friendly phrasing.
- The result header shows per-source hit counts; a source at 0 may be a
  transient failure — a retry is cheap.
- Cite only what the tools returned. Never invent citations or links.
- For a durable writeup, call `export_research_tool`, save the returned
  LaTeX to a `.tex` file, and compile with `pdflatex` if available.

Full guidance: `.agents/skills/digilib/SKILL.md`.

## Repository layout

```
digilib_mcp/                     the server (server.py, config.py, services/, digiexport.py, auth.py)
digilib_mcp/context/             researcher.md — the DigiLIB persona prompt
.agents/skills/digilib/          canonical skill (symlinked into agent skills dirs)
docs/agents/                     per-agent connection guides
demo/                            demo recording (Claude Desktop)
Digilib citation manager landing/  landing-page design mockups
pyproject.toml                   packaging (console script: digilib-mcp)
```

## Conventions

- Keep it keyless: no required API keys, no paid services, no secrets.
- No personal data, personal emails, or machine-specific paths in the repo.
- Python 3.10+; stdio is the default transport, `streamable-http` optional.
- The agent-specific skill directories (`.claude/skills`, `.antigravitycli/skills`,
  `.grok/skills`, `.kimi/skills`, `.opencode/skills`, `.qwen/skills`) contain
  symlinks to `.agents/skills/digilib/SKILL.md` — edit the canonical file
  only, never the symlinks.
