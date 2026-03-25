---
description: Save something to Astria's persistent memory
---

Save information to persistent memory using the Astria `remember` tool.

When the user says `/remember`, they want to save something important. Follow these steps:

1. If the user provided text after `/remember`, use that as the content
2. If not, ask what they'd like to remember

3. Call the `remember` MCP tool with:
   - `content`: The text to remember
   - `category`: Choose the best fit — `fact`, `decision`, `preference`, `idea`, `project`, or `person`
   - `importance`: Use `high` if it's something that should always be recalled, otherwise omit

4. Confirm what was saved with a brief summary

Example: `/remember We decided to use Supabase instead of Clerk for auth`
→ Calls `remember` with category "decision", confirms save
