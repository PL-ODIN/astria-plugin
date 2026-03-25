---
description: Connect Astria to Claude Code — set your endpoint and API key
disable-model-invocation: true
---

# Astria Setup

Set up your Astria persistent memory connection. You'll need your endpoint URL and API key from https://astriaindex.com/dashboard

## Steps

1. Ask the user for their **Astria Endpoint** (e.g., `https://u443d37ca.astriaindex.com`)
   - If they don't have one, direct them to https://astriaindex.com to sign up

2. Ask the user for their **Astria API Key** (starts with `astria_`)
   - If they don't have one, they can generate one at https://astriaindex.com/dashboard under the Connect tab

3. Once you have both values, set them as environment variables by adding to the user's shell profile or by running:

```bash
export ASTRIA_ENDPOINT="<their endpoint>"
export ASTRIA_API_KEY="<their API key>"
```

4. Also add them to the project's `.claude/settings.local.json`:

```json
{
  "env": {
    "ASTRIA_ENDPOINT": "<their endpoint>",
    "ASTRIA_API_KEY": "<their API key>"
  }
}
```

5. Tell the user to restart Claude Code. On restart, the Astria MCP server will connect automatically.

6. Verify the connection by running: `/astria-stats`

## Important
- Never commit API keys to git. The `.claude/settings.local.json` file should be in `.gitignore`.
- If the user doesn't have an account yet, direct them to https://astriaindex.com
