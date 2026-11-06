# digilib in Hermes Agent

## Register

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  digilib:
    command: "uvx"
    args: ["--from", "git+https://github.com/cars3/digilib-mcp", "digilib-mcp"]
```

Or use the interactive CLI route — `hermes mcp add digilib` (it connects,
discovers the tools, and asks which to enable; on a headless run, pipe the
confirmation: `printf 'Y\n' | hermes mcp add ...`).

## Use

Restart Hermes Agent. The tools are auto-discovered and appear as
`mcp_digilib_search_papers`, `mcp_digilib_search_books`, and
`mcp_digilib_export_research_tool` in every session.

## Verify

```bash
hermes mcp list
hermes mcp test digilib
```
