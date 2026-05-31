# Recommended MCP Servers for Hermes (Symbiosis Enhancement)

Adding these to Hermes gives it tool parity and superpowers that complement Grok Build's strengths (especially the rich grok_com_github MCP available in Grok sessions).

## GitHub (Highest Priority for Symbiosis)

```bash
hermes mcp add github \
  --command npx \
  --args "-y @modelcontextprotocol/server-github" \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
```

- Gives Hermes `github__create_issue`, `github__search_code`, `github__list_pull_requests`, etc.
- Pairs beautifully with Grok's `grok_com_github` (42 tools) when you escalate between the two.
- Use the GitHub token from `~/Documents/Github_Hermes_Token.txt` (or a fresh one with appropriate scopes: repo, read:org, etc.).

After adding:
```bash
hermes mcp list
hermes mcp test github
```

## Other High-Value Additions

### Filesystem (scoped, safe)
```bash
hermes mcp add workspace-fs \
  --command npx \
  --args "-y @modelcontextprotocol/server-filesystem /home/Irikash"
```

### Git (local repo operations)
```bash
hermes mcp add git \
  --command npx \
  --args "-y @modelcontextprotocol/server-git"
```

### Playwright / Browser automation (if available)
```bash
hermes mcp add browser \
  --command npx \
  --args "-y @modelcontextprotocol/server-puppeteer"
```

Or use Hermes' own strong browser tools + Tool Gateway if on Nous Portal.

### SQLite / Postgres (project databases)
Useful for data-heavy work where Grok or Hermes needs to query local dbs.

## How This Strengthens the Symbiosis

- **Grok sessions**: Leverage the custom `grok_com_github` (very rich) + any other MCPs registered in `~/.grok/config.toml` for heavy GitHub / external work.
- **Hermes sessions**: Use the standard GitHub MCP (and others) you add here for the same class of operations when running autonomously or via gateway.
- **Handoffs**: Either side can perform GitHub-heavy actions without the other; when one side starts something complex, it can hand off cleanly knowing the other has equivalent (or specialized) tooling.

## Quick Add Script (example)

```bash
# After setting GITHUB_TOKEN env or editing the command
hermes mcp add github --command npx --args "-y @modelcontextprotocol/server-github" --env GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_TOKEN"
```

See also: `hermes mcp --help` and the main symbiosis README.
