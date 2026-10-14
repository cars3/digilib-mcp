# digilib in Gemini CLI (legacy)

Gemini CLI consumer access has transitioned to Antigravity CLI, which reads
the same `~/.gemini` configuration tree — see [antigravity.md](antigravity.md)
for the current setup.

If you're still on Gemini CLI, add to `~/.gemini/settings.json`:

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

Verify with `/mcp` inside a session. For new setups, prefer Antigravity.
