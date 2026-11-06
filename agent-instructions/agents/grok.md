# digilib in Grok CLI

## Register

Add to `~/.grok/config.toml`:

```toml
[mcp_servers.digilib]
command = "uvx"
args = ["--from", "git+https://github.com/cars3/digilib-mcp", "digilib-mcp"]
```

Or via the CLI:

```bash
grok mcp add digilib -- uvx --from git+https://github.com/cars3/digilib-mcp digilib-mcp
```

Project-scoped servers live in `.grok/config.toml` — add `--scope project`
to `grok mcp add`.

## Verify

```bash
grok mcp list
grok mcp doctor digilib     # connectivity check
```

## Notes

- Grok also loads MCP configs from `~/.claude.json`, `.cursor/mcp.json`,
  and project `.mcp.json` files (compatibility), merged below its own
  `config.toml`.
- Working inside the digilib-mcp checkout? The bundled skill is at
  `.grok/skills/digilib/SKILL.md`.
