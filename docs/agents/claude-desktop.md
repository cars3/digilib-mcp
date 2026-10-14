# digilib in Claude Desktop

## 1. Edit the config

Add digilib under `mcpServers` in `claude_desktop_config.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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

Add it alongside any servers already listed — don't replace them.

## 2. Restart Claude Desktop completely

Quit the app fully (macOS: Cmd+Q — closing the window is not enough) and
reopen it. Claude Desktop reads its config only at launch.

## Verify

digilib should appear in the tools menu with `search_papers`,
`search_books`, and `export_research_tool`; Desktop asks you to approve each
call the first time. Then ask: "Search arXiv and OpenAlex for recent papers
on X."

## Troubleshooting

- **`uvx` not found**: Desktop doesn't always inherit your shell PATH. Run
  `which uvx` in a terminal and replace `"command": "uvx"` with that
  absolute path.
- **digilib doesn't appear at all**: fully quit and reopen (see step 2).
- Server log (macOS): `~/Library/Logs/Claude/mcp-server-digilib.log`.

## Notes

Don't have uv/uvx? Install it: `curl -LsSf https://astral.sh/uv/install.sh | sh`
(or `brew install uv`).
