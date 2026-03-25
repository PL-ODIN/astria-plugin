---
description: Show your Astria memory statistics — memories, sessions, insights, and notes
---

Show the user's Astria memory statistics.

When the user says `/astria-stats`:

1. Call the `my_memory_stats` MCP tool
2. Present the stats in a clean summary:

   **Your Astria Memory**
   - Memories: total count + breakdown by category
   - Sessions: active + completed
   - Notes: count
   - Insights: count (learned patterns)

3. If there are active sessions, list them with their descriptions
4. If memory is empty, suggest:
   - Use `/remember` to save important facts and decisions
   - Use `/session start` to begin tracking work
   - Memory grows naturally as you work — the AI learns from every conversation

This also serves as a connection test. If the MCP tool call fails, the Astria connection isn't configured. Direct the user to run `/astria-setup`.
