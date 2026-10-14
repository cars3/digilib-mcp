# digilib in any MCP client

digilib is a standard stdio MCP server. The values are always the same:

- command: `uvx`
- args: `--from git+https://github.com/cars3/digilib-mcp digilib-mcp`

Most clients accept a JSON shape like:

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

## Shape variations to watch for

- Top-level key: `mcpServers` (most clients), `mcp` (OpenCode), `servers`
  (VS Code Copilot)
- Type field: some clients require `"type": "local"` or `"type": "stdio"`
- Single-array command: some clients want `"command": ["uvx", "--from", ...]`

The three values never change; only the packaging differs.

## Alternative ways to run it

1. **Installed from git** (equivalent to uvx):

   ```bash
   pip install "git+https://github.com/cars3/digilib-mcp"
   ```

   then use command `digilib-mcp`.

2. **From a checkout**:

   ```json
   {
     "mcpServers": {
       "digilib": {
         "command": "/path/to/digilib-mcp/.venv/bin/python",
         "args": ["-m", "digilib_mcp.server"],
         "cwd": "/path/to/digilib-mcp"
       }
     }
   }
   ```

3. **HTTP** (remote or shared): start the gateway with
   `DIGILIB_TRANSPORT=streamable-http python -m digilib_mcp.server` and point
   the client at `http://<host>:8000/mcp`.

## Verify

Once registered, ask the agent to run a search — e.g. "Use digilib to find
recent papers on X."
