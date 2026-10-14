# digilib in Codex

## Register

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.digilib]
command = "uvx"
args = ["--from", "git+https://github.com/cars3/digilib-mcp", "digilib-mcp"]
```

If your Codex build ships MCP management commands, the CLI route works too
(check `codex mcp --help` for your version):

```bash
codex mcp add digilib -- uvx --from git+https://github.com/cars3/digilib-mcp digilib-mcp
```

## Use

Slash commands aren't guaranteed in Codex — phrase it in a prompt:

```text
Use the digilib tools to find recent papers on X and summarize the top hits.
```

Headless workers use `codex exec`:

```bash
codex exec "Use digilib to find three recent papers on speculative decoding and summarize them"
```

Working inside the digilib-mcp checkout, Codex loads `AGENTS.md` as project
context, which points at the digilib skill.

## Verify

Start a session and ask: "Which digilib tools do you have?" — expect
`search_papers`, `search_books`, `export_research_tool`.
