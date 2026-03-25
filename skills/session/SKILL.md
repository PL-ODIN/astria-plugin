---
description: Start, resume, or end an Astria working session for cross-conversation continuity
---

Manage Astria sessions for cross-conversation continuity.

When the user says `/session`, check what they want:

## Start a new session
If the user says `/session start <description>` or just `/session` with no active sessions:
1. Call `start_session` with a brief description of the work
2. Confirm the session ID and what's being tracked

## Resume an existing session
If the user says `/session resume` or `/session resume <id>`:
1. Call `my_sessions` to list active sessions
2. If there's only one, resume it automatically with `resume_session`
3. If multiple, show the list and ask which one
4. After resuming, briefly summarize where they left off

## End a session
If the user says `/session end`:
1. Call `end_session` with a summary of what was accomplished
2. Ask if any key learnings should be promoted to permanent memory
3. If yes, call `promote_session`

## List sessions
If the user says `/session list`:
1. Call `my_sessions`
2. Show active sessions with their descriptions and status

Example: `/session resume` → Shows active sessions, resumes the selected one with full context
