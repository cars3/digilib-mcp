# digilib in Cursor

## Register

Add to `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

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

Cursor → Settings → MCP should list digilib as connected. Then ask the
Agent: "Use digilib to search for recent papers on X."

## Notes

- Cursor prompts for approval on tool calls by default.
- Working inside the digilib-mcp checkout, Cursor auto-discovers the bundled
  skill from the shared `.agents/skills/digilib/` layout.
