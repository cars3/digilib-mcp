# digilib in Windsurf

## Register

Edit `~/.codeium/windsurf/mcp_config.json` (create it if missing):

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

## Verify

Windsurf → Cascade → MCP servers: digilib should be listed and running.
Then ask Cascade: "Use digilib to search for recent papers on X."

## Notes

- Use the absolute path to `uvx` (`which uvx`) if Windsurf can't find it on
  its PATH.
