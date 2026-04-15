# Astria — Persistent AI Memory

## Description
AI memory that works like yours. Neural pathway architecture gives your AI persistent recall, contextual awareness, and cross-session continuity. Your AI never starts from zero again.

## Category
Knowledge & Memory

## Tags
memory, knowledge-graph, persistent-memory, semantic-search, sessions, recall, neo4j, pgvector, cross-session, mcp

## Setup

### Prerequisites
- An Astria account ([sign up at astriaindex.com](https://astriaindex.com))
- Your API key and endpoint (from the [dashboard](https://astriaindex.com/dashboard))

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `ASTRIA_API_KEY` | Yes | Your Astria API key from the dashboard |
| `ASTRIA_ENDPOINT` | Yes | Your dedicated memory endpoint URL |

### Install (Claude Code)
```
/plugin marketplace add PL-ODIN/astria-plugin
/plugin install astria@astria-marketplace
/astria-setup
```

### Install (Any MCP Client)
```json
{
  "mcpServers": {
    "astria": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://YOUR_ENDPOINT/sse"],
      "env": {
        "ASTRIA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Tools (15)

| Tool | Description |
|------|-------------|
| `remember` | Save facts, decisions, preferences, ideas to persistent memory |
| `recall` | Search memories by meaning using semantic similarity |
| `forget` | Remove a specific memory permanently |
| `list_memories` | Browse stored memories, most recent first |
| `my_memory_stats` | Overview of your memory network statistics |
| `record_insight` | Record cause-and-effect patterns for future reference |
| `my_insights` | Browse discovered patterns ranked by frequency |
| `start_session` | Start a working session for cross-conversation continuity |
| `resume_session` | Resume a previous session with full context |
| `end_session` | End a session and record what was accomplished |
| `my_sessions` | List active sessions you can resume |
| `promote_session` | Save key session learnings as permanent memories |
| `save_note` | Save a named note for exact retrieval |
| `get_note` | Retrieve a saved note by name |
| `getting_started` | Get the complete Astria operating guide |

## Architecture
Each subscriber gets dedicated, physically isolated infrastructure:
- **Neo4j** knowledge graph for structured memory and relationships
- **pgvector** with OpenAI embeddings for semantic search
- **Redis** for working memory, sessions, and real-time state

Your data is never shared or mixed with other users.

## Pricing
**$50/month** — unlimited memories, unlimited sessions, unlimited recall. One price. No tiers. No metering.

## Links
- [Website](https://astriaindex.com)
- [Dashboard](https://astriaindex.com/dashboard)
- [GitHub](https://github.com/PL-ODIN/astria-plugin)
- [Glama](https://glama.ai/mcp/servers/PL-ODIN/astria-plugin)
