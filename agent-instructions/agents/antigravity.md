# digilib in Antigravity (CLI / IDE / 2.0)

Antigravity tools share one MCP configuration, so registering digilib once
makes it available across the suite.

## Global (all workspaces)

Edit `~/.gemini/config/mcp_config.json`:

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

## Per project

Same JSON in `.agents/mcp_config.json` at the project root.

## Newer CLI shortcut

Antigravity CLI 1.1.16+ has an `mcp` subcommand:

```bash
agy mcp add digilib -- uvx --from git+https://github.com/cars3/digilib-mcp digilib-mcp
```

## Skills

Working inside the digilib-mcp checkout, Antigravity auto-discovers the
bundled skill at `.antigravitycli/skills/digilib/SKILL.md`.

## Verify

Open the MCP manager (or the CLI's MCP list) and confirm digilib shows as
connected with three tools, then ask for a literature search.

## Notes

- Antigravity's config format also supports remote servers via `serverUrl`
  if you self-host the streamable-http gateway — the stdio form above is the
  simple path.
- The config lives under `~/.gemini/` (shared with older Gemini tooling);
  skills may also be placed globally at `~/.gemini/skills/`.
