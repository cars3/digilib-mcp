# digilib-mcp — Agent Guide

**DigiLIB stands for "digital librarian".** This repository is an MCP server
that gives the ability of a digital librarian to the agent of choice: search
academic papers and books across six free sources, and export a cited
literature review as LaTeX.

This file is the canonical instruction file for AI coding agents working in,
with, or on this repository. It lives in `agent-instructions/` together with
the agent skill and the per-agent connection guides.

The repository root carries thin pointers (`AGENTS.md`, `CLAUDE.md`,
`CODEX.md`, `KIMI.md`, `OPENCODE.md`) that import this file, plus symlinked
agent directories (`.agents`, `.claude`, `.antigravitycli`, `.grok`,
`.kimi`, `.opencode`, `.qwen`) that point into this folder. Those exist only
so every agent still auto-discovers the instructions. Edit the files here,
never the root pointers or symlinks.

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

One-page registration guides for every supported agent:
`agent-instructions/agents/`.

| Agent | Registration location | Guide |
|---|---|---|
| Claude Code | `.mcp.json` / `claude mcp add` | [agents/claude-code.md](agents/claude-code.md) |
| Claude Desktop | `claude_desktop_config.json` | [agents/claude-desktop.md](agents/claude-desktop.md) |
| Codex | `~/.codex/config.toml` | [agents/codex.md](agents/codex.md) |
| Antigravity (CLI / IDE / 2.0) | `~/.gemini/config/mcp_config.json`, `.agents/mcp_config.json` | [agents/antigravity.md](agents/antigravity.md) |
| Cursor | `.cursor/mcp.json` | [agents/cursor.md](agents/cursor.md) |
| OpenCode | `opencode.json(c)` | [agents/opencode.md](agents/opencode.md) |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | [agents/windsurf.md](agents/windsurf.md) |
| Qwen Code | `~/.qwen/settings.json` | [agents/qwen.md](agents/qwen.md) |
| Kimi CLI | `~/.kimi/mcp.json` | [agents/kimi.md](agents/kimi.md) |
| Grok CLI | `~/.grok/config.toml` | [agents/grok.md](agents/grok.md) |
| GitHub Copilot CLI | `~/.copilot/mcp-config.json` | [agents/copilot-cli.md](agents/copilot-cli.md) |
| Pi | `~/.pi/agent/mcp.json` (`pi mcp add`) | [agents/pi.md](agents/pi.md) |
| Hermes Agent | `~/.hermes/config.yaml` (`mcp_servers`) | [agents/hermes.md](agents/hermes.md) |
| Gemini CLI (legacy) | see guide | [agents/gemini-cli.md](agents/gemini-cli.md) |
| Any other MCP client | standard stdio pattern | [agents/generic.md](agents/generic.md) |

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

Full guidance: `agent-instructions/.agents/skills/digilib/SKILL.md`.

## Repository layout

```
agent-instructions/                agent instructions: readmes, skill, connection guides
agent-instructions/AGENTS.md       this file, the canonical guide
agent-instructions/agents/         per-agent connection guides
agent-instructions/.agents/skills/digilib/  canonical agent skill
digilib_mcp/                       the server (server.py, config.py, services/, digiexport.py, auth.py)
digilib_mcp/context/               researcher.md — the DigiLIB persona prompt
demo/                              demo recording (Claude Desktop)
Digilib citation manager landing/  landing-page design mockups
pyproject.toml                     packaging (console script: digilib-mcp)
```

## Conventions

- Keep it keyless: no required API keys, no paid services, no secrets.
- No personal data, personal emails, or machine-specific paths in the repo.
- Python 3.10+; stdio is the default transport, `streamable-http` optional.
- The root agent directories (`.claude`, `.antigravitycli`, `.grok`, `.kimi`,
  `.opencode`, `.qwen`) are symlinks to `agent-instructions/`. Inside that
  folder, each agent's `skills/digilib/SKILL.md` is a symlink to
  `.agents/skills/digilib/SKILL.md` — edit the canonical skill only, never
  the symlinks or the root pointers.
