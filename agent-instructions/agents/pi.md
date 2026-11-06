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

The bundled skill lives at `agent-instructions/SKILL.md`; Pi can load it
directly when working inside the checkout.
