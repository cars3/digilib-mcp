# Connecting digilib to your agent

digilib is a standard stdio MCP server (Python, distributed via `uvx`).
Pick your agent's guide below — each has an exact config location, a
paste-ready snippet, and a verification step.

| Agent | Guide |
|---|---|
| Claude Code | [claude-code.md](claude-code.md) |
| Claude Desktop | [claude-desktop.md](claude-desktop.md) |
| Codex CLI | [codex.md](codex.md) |
| Antigravity (CLI / IDE / 2.0) | [antigravity.md](antigravity.md) |
| Cursor | [cursor.md](cursor.md) |
| OpenCode | [opencode.md](opencode.md) |
| Windsurf | [windsurf.md](windsurf.md) |
| Qwen Code | [qwen.md](qwen.md) |
| Kimi CLI | [kimi.md](kimi.md) |
| Grok CLI | [grok.md](grok.md) |
| GitHub Copilot CLI | [copilot-cli.md](copilot-cli.md) |
| Pi | [pi.md](pi.md) |
| Hermes Agent | [hermes.md](hermes.md) |
| Gemini CLI (legacy) | [gemini-cli.md](gemini-cli.md) |
| Any other MCP client | [generic.md](generic.md) |

## The universal settings

Every guide below reduces to the same three values:

- command: `uvx`
- args: `--from git+https://github.com/cars3/digilib-mcp digilib-mcp`
- transport: stdio

If your agent isn't listed, use [generic.md](generic.md) — the values above
work with any MCP client once you know its config file format.

## No keys, no environment variables

digilib needs no API keys or env vars. (Optional settings — a polite-pool
email for OpenAlex, a Google Books quota key — live in `.env`; see the main
README's Configuration section.)
