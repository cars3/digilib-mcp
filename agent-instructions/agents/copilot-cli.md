# digilib in GitHub Copilot CLI

## Register

Edit `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "digilib": {
      "type": "local",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/cars3/digilib-mcp", "digilib-mcp"],
      "tools": ["*"]
    }
  }
}
```

Per-repository, Copilot CLI reads `.mcp.json` at the project root or
`.github/mcp.json` (committable). You can also manage servers in-session
with `/mcp add`.

## Verify

Run `/mcp` in a session (or the `copilot mcp` subcommands) and confirm
digilib is enabled; then ask for a literature search.

## Notes

- Project-level servers load only after you confirm folder trust on first
  launch.
