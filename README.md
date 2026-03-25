# Astria — Persistent AI Memory

Your AI never starts from zero again. Astria is a persistent memory layer that works across sessions, tools, and time.

Every insight compounds. Every session builds on the last. Switch between Claude Code, Cursor, Windsurf, or any MCP-compatible client — your memory follows you.

## Install (Claude Code)

```
/plugin marketplace add PL-ODIN/astria-plugin
/plugin install astria@astria-marketplace
/astria-setup
```

That's it. Three commands.

## What you get

| Command | What it does |
|---|---|
| `/remember` | Save a fact, decision, preference, or idea to permanent memory |
| `/recall` | Search your memory using natural language |
| `/session` | Start, resume, or end working sessions for cross-conversation continuity |
| `/astria-stats` | View your memory statistics — how much your AI knows |

## How it works

Astria runs as an MCP server connected to your own dedicated memory infrastructure. When you save a memory, it's stored in a knowledge graph with semantic embeddings. When you recall, Astria searches by meaning — not just keywords.

Sessions give you continuity across conversations. Start a session today, close Claude Code, come back next week — pick up exactly where you left off.

### Memory types

- **Facts** — things that are true ("our API uses OAuth2")
- **Decisions** — choices you've made ("we chose Postgres over Mongo")
- **Preferences** — how you like to work ("I prefer concise responses")
- **Ideas** — things to explore later ("consider adding WebSocket support")
- **Projects** — ongoing work context ("migrating from v1 to v2 API")
- **Insights** — learned patterns ("when X happens, the cause is usually Y")

## Works with any MCP client

While the plugin is optimized for Claude Code, Astria works with any tool that supports MCP over SSE:

- **Claude Code** — Plugin install (recommended)
- **Claude Desktop** — Add MCP server in settings
- **Cursor** — MCP server config
- **Windsurf** — MCP server config

See [manual setup instructions](https://astriaindex.com/dashboard) after signing up.

## Pricing

**$50/month** — unlimited memories, unlimited sessions, unlimited recall. One price. No tiers. No metering.

Each subscriber gets their own dedicated, physically isolated memory infrastructure. Your data is never shared or mixed with other users.

## Get started

1. Sign up at [astriaindex.com](https://astriaindex.com)
2. Install the plugin (see above)
3. Run `/astria-setup` and paste your endpoint + API key
4. Start remembering

## Links

- [Website](https://astriaindex.com)
- [Dashboard](https://astriaindex.com/dashboard)
- [Terms of Service](https://astriaindex.com/terms)
- [Privacy Policy](https://astriaindex.com/privacy)
