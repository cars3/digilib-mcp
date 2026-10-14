# digilib in Pi

## Register

```bash
pi mcp add digilib -- uvx --from git+https://github.com/cars3/digilib-mcp digilib-mcp
```

This writes the global server list at `~/.pi/agent/mcp.json`.

## Verify

```bash
pi mcp list      # digilib should appear with 3 tools
```

## Skills

Working inside the digilib-mcp checkout, Pi auto-discovers the skill from
`.agents/skills/digilib/` and exposes it as `/skill:digilib`.
