# digilib in Claude Code

## Register

Quickest — the CLI:

```bash
claude mcp add digilib -- uvx --from git+https://github.com/cars3/digilib-mcp digilib-mcp
```

Or add it to `.mcp.json` at your project root (alongside any servers already
listed — don't replace them):

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

## Use

Ask naturally: "Search the literature on X with digilib, and pull two books
on Y." Claude Code calls `search_papers` / `search_books` /
`export_research_tool` as needed.

Working inside the digilib-mcp checkout? Claude Code also auto-discovers the
bundled skill at `.claude/skills/digilib/SKILL.md`, which teaches the
research workflow.

## Verify

```bash
claude mcp list     # digilib should be listed and connected
```

Then ask: "Use digilib to search arXiv for recent papers on speculative
decoding."

## Notes

- No keys or env vars needed.
- The server speaks stdio; Claude Code launches it on demand.
