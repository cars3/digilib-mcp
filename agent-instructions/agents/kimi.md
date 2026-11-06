# digilib in Kimi CLI

## Register

Add to `~/.kimi/mcp.json` (create it if missing; servers added via
`kimi mcp add` are stored here too):

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

`kimi mcp add` is the CLI route — run `kimi mcp add --help` for the exact
form on your version.

## Skills

Kimi merges skills from all brand directories by default
(`merge_all_available_skills: true`), so the bundled skill at
`.kimi/skills/digilib/SKILL.md` is available when working inside the repo.

## Verify

Ask: "List the tools digilib provides" — expect `search_papers`,
`search_books`, `export_research_tool`.
