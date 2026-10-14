# digilib in OpenCode

## Register

OpenCode uses the `mcp` key (not `mcpServers`), and every entry needs a
`type`. Add to `opencode.json` at your project root, or to
`~/.config/opencode/opencode.json` for all projects:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "digilib": {
      "type": "local",
      "command": ["uvx", "--from", "git+https://github.com/cars3/digilib-mcp", "digilib-mcp"],
      "enabled": true
    }
  }
}
```

Working inside the digilib-mcp checkout, the bundled slash command
`.opencode/commands/digilib.md` is auto-registered — `/digilib` loads the
skill.

## Verify

```bash
opencode mcp list     # digilib should appear, connected
```

Then ask: "Use digilib to find papers on X."

## Notes

Newer OpenCode builds may nest servers as `mcp.servers.<name>` — if your
config validator rejects the form above, check `opencode.ai/docs` for your
version's shape.
