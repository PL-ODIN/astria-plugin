---
description: Search Astria's persistent memory for relevant context
---

Search persistent memory using the Astria `recall` tool.

When the user says `/recall`, they want to find something from their memory. Follow these steps:

1. If the user provided a query after `/recall`, use that as the search
2. If not, ask what they're looking for

3. Call the `recall` MCP tool with:
   - `query`: Natural language search (e.g., "auth decisions", "deployment issues", "project architecture")
   - `limit`: Default 5, increase if user wants more results

4. Present the results clearly:
   - Show each memory with its category, importance, and a brief preview
   - If results include insights (causal patterns), highlight the symptom → cause → resolution
   - If no results found, suggest broadening the search terms

Example: `/recall deployment failures`
→ Calls `recall`, shows matching memories about past deployment issues
