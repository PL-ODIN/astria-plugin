"""Astria MCP Server — thin proxy to your dedicated Astria instance.

Connects to your Astria memory infrastructure via SSE and exposes
all tools locally. Used by Glama for inspection and by MCP clients
that prefer local stdio transport.
"""

import os
import sys
from typing import Optional

from fastmcp import Client, FastMCP
from fastmcp.client.transports import SSETransport

ENDPOINT = os.environ.get("ASTRIA_ENDPOINT", "")
API_KEY = os.environ.get("ASTRIA_API_KEY", "")

if not ENDPOINT:
    print("ASTRIA_ENDPOINT is required. Get yours at https://astriaindex.com/dashboard", file=sys.stderr)
    sys.exit(1)

sse_url = ENDPOINT.rstrip("/")
if not sse_url.endswith("/sse"):
    sse_url += "/sse"

mcp = FastMCP("Astria")


# ── Memory ──────────────────────────────────────────────────────────

@mcp.tool()
async def remember(content: str, category: Optional[str] = None, importance: str = "normal") -> str:
    """Save something to your long-term memory.

    Anything you save here persists forever and can be found later with `recall`
    by searching for its meaning — not just exact words. Every memory is stored
    in a knowledge graph with semantic embeddings.

    Use this when:
    - You learn a fact worth keeping: `remember("Our API uses OAuth2 with PKCE", category="fact")`
    - A decision is made: `remember("Chose Postgres over Mongo for ACID compliance", category="decision", importance="high")`
    - You discover a user preference: `remember("User prefers concise responses", category="preference")`
    - An idea comes up: `remember("Consider adding WebSocket support for real-time sync", category="idea")`

    Args:
        content: What to remember — facts, decisions, preferences, ideas, project context.
            Be specific and include reasoning when possible.
        category: Tag for organization. One of: preference, fact, decision, idea, project, person, general.
            If omitted, auto-categorized as "general".
        importance: Priority level — "low", "normal", or "high".
            High-importance memories surface first in recall results.

    Returns:
        Confirmation with the assigned memory ID. Returns an error message
        if the content is empty or the server is unreachable.
    """
    return await _proxy("remember", content=content, category=category, importance=importance)


@mcp.tool()
async def recall(query: str, limit: int = 5, category: Optional[str] = None) -> str:
    """Search your memories by meaning, not keywords.

    Uses semantic similarity to find the most relevant memories you've saved.
    Results are ranked by how closely they match your query.

    Use this when:
    - Looking up a past decision: `recall("what database did we choose?")`
    - Checking what you know about a topic: `recall("authentication setup")`
    - Finding a specific fact: `recall("API rate limits", category="fact")`
    - Starting a new conversation: `recall("current project status")` to get context

    Args:
        query: What you're looking for, in natural language. Longer, more specific
            queries produce better results than single words.
        limit: Maximum results to return (default 5, max 20). Use higher limits
            when exploring a broad topic.
        category: Optional filter — only return memories tagged with this category.
            One of: preference, fact, decision, idea, project, person, general.

    Returns:
        A ranked list of matching memories with their IDs, content, category,
        importance, and similarity score. Returns an empty list if no matches found.
        Returns an error message if the server is unreachable.
    """
    return await _proxy("recall", query=query, limit=limit, category=category)


@mcp.tool()
async def forget(memory_id: str) -> str:
    """Remove a specific memory permanently from your knowledge graph.

    This action is irreversible — the memory and its embeddings are deleted.
    Use `recall` or `list_memories` first to find the correct memory_id.

    Use this when:
    - A fact is no longer true: `forget("mem_abc123")`
    - A decision was reversed and the old one is misleading
    - Removing duplicate or incorrect memories

    Do NOT use this to "update" a memory — instead, forget the old one
    and `remember` the corrected version.

    Args:
        memory_id: The unique memory identifier (e.g., "mem_abc123") obtained
            from `remember`, `recall`, or `list_memories` results.

    Returns:
        Confirmation that the memory was deleted. Returns an error if the
        memory_id doesn't exist or has already been deleted.
    """
    return await _proxy("forget", memory_id=memory_id)


@mcp.tool()
async def list_memories(category: Optional[str] = None, limit: int = 20) -> str:
    """Browse your stored memories, ordered most recent first.

    Unlike `recall` which searches by meaning, this returns memories
    in chronological order — useful for reviewing recent activity.

    Use this when:
    - Browsing recent memories: `list_memories(limit=10)`
    - Reviewing all decisions: `list_memories(category="decision")`
    - Checking what's been stored: `list_memories(category="project", limit=50)`
    - Auditing memory before cleanup

    Args:
        category: Optional filter — only return memories with this tag.
            One of: preference, fact, decision, idea, project, person, general.
            Omit to see all categories.
        limit: How many to return (default 20, max 100).

    Returns:
        A list of memories with IDs, content, category, importance, and timestamps.
        Returns an empty list if no memories exist (or none match the filter).
    """
    return await _proxy("list_memories", category=category, limit=limit)


# ── Reflect ─────────────────────────────────────────────────────────

@mcp.tool()
async def my_memory_stats() -> str:
    """See a dashboard overview of your entire memory network.

    Shows total counts broken down by category, plus active sessions,
    saved notes, learned insights, and embedding statistics.

    Use this when:
    - Starting a conversation to understand what's in memory
    - Checking if memory is growing as expected
    - Reporting on memory utilization: `my_memory_stats()`

    Returns:
        A statistics object with memory counts by category, session counts
        (active vs completed), note count, insight count, and embedding count.
        All counts are zero for a fresh instance.
    """
    return await _proxy("my_memory_stats")


# ── Insights ────────────────────────────────────────────────────────

@mcp.tool()
async def record_insight(pattern: str, cause: str, solution: str, confidence: float = 0.7) -> str:
    """Record a cause-and-effect pattern you've discovered.

    Insights are the deepest memory tier — understanding WHY things happen.
    Over time, your memory builds a library of patterns that surface
    automatically when similar situations recur. If the same pattern+cause
    is recorded again, the confidence score increments rather than creating
    a duplicate.

    Use this when:
    - A recurring bug is explained: `record_insight("deploys fail on Fridays", "cache expires weekly", "flush cache before Friday deploys")`
    - A workflow pattern emerges: `record_insight("PR reviews take 3+ days", "no reviewer assigned", "auto-assign reviewers on PR creation")`
    - A root cause is found after investigation

    Args:
        pattern: The observable symptom or recurring situation.
        cause: The root cause — why this happens.
        solution: How to fix or prevent it.
        confidence: How certain you are this cause is correct (0.0 to 1.0).
            Use 0.5 for hypotheses, 0.7 for likely, 1.0 for confirmed.

    Returns:
        The insight ID and how many times this exact pattern has been observed.
        If this pattern+cause was seen before, returns the updated confidence count.
    """
    return await _proxy("record_insight", pattern=pattern, cause=cause, solution=solution, confidence=confidence)


@mcp.tool()
async def my_insights(limit: int = 20) -> str:
    """Browse your discovered cause-and-effect patterns.

    Returns insights ranked by observation frequency — patterns seen
    multiple times appear first, indicating higher reliability.

    Use this when:
    - Reviewing known patterns before debugging: `my_insights(limit=10)`
    - Checking if a similar issue was seen before
    - Building a knowledge base of recurring problems and solutions
    - Onboarding someone to a project's known quirks

    Args:
        limit: Maximum insights to return (default 20, max 50).

    Returns:
        A list of insights with pattern, cause, solution, confidence score,
        and observation count. Returns an empty list if no insights recorded yet.
    """
    return await _proxy("my_insights", limit=limit)


# ── Sessions ────────────────────────────────────────────────────────

@mcp.tool()
async def start_session(description: str) -> str:
    """Start a working session for cross-conversation continuity.

    Sessions let you pick up exactly where you left off, even days or weeks
    later in a completely new conversation. A session tracks your goal,
    progress, and related memories.

    Use this when:
    - Beginning multi-step work: `start_session("Migrating auth from JWT to OAuth2")`
    - Starting a research task: `start_session("Investigating memory leak in worker service")`
    - Any work that will span multiple conversations

    Do NOT start a session for quick, single-conversation tasks.
    Call `my_sessions` first to check for existing sessions to resume.

    Args:
        description: What you're working on — stored verbatim and used to
            restore context when resuming. Be specific enough that you'll
            understand the goal when you come back later.

    Returns:
        A session ID (e.g., "s001") to use with `resume_session`, `end_session`,
        and `promote_session`. Returns an error if description is empty.
    """
    return await _proxy("start_session", description=description)


@mcp.tool()
async def resume_session(session_id: str) -> str:
    """Resume a previous session and get full context to continue working.

    Retrieves the session's description, progress, related memories, notes,
    and any sub-tasks — everything needed to continue where you left off.

    Use this when:
    - Starting a new conversation and `my_sessions` shows active work: `resume_session("s001")`
    - Returning to a task after a break
    - Checking progress on ongoing work

    Always call `my_sessions` first to find the correct session_id.

    Args:
        session_id: The session identifier (e.g., "s001") from `start_session`
            or `my_sessions` results.

    Returns:
        Full session context including description, status, timestamps, related
        memories, notes, and progress. Returns an error if the session_id
        doesn't exist or has already been completed.
    """
    return await _proxy("resume_session", session_id=session_id)


@mcp.tool()
async def end_session(session_id: str, summary: Optional[str] = None) -> str:
    """End a session and record what was accomplished.

    Marks the session as completed and optionally saves a summary.
    Consider calling `promote_session` first to save key learnings
    as permanent memories before ending.

    Use this when:
    - Work is finished: `end_session("s001", summary="Auth migration complete, all tests passing")`
    - Abandoning a session: `end_session("s001", summary="Deprioritized — will revisit Q3")`
    - Wrapping up for the day with a status update

    The session data is retained for 48 hours after completion, then
    auto-expires. Promoted memories persist forever.

    Args:
        session_id: The session to complete (e.g., "s001").
        summary: Optional final summary of the outcome. If omitted, the session
            closes without a summary. Include what was accomplished and any
            follow-up items.

    Returns:
        The final session state with status "completed". Returns an error
        if the session doesn't exist or was already ended.
    """
    return await _proxy("end_session", session_id=session_id, summary=summary)


@mcp.tool()
async def my_sessions() -> str:
    """List all active sessions you can resume.

    Call this at the start of every new conversation to check for
    interrupted work. If sessions exist, use `resume_session` to
    continue where you left off.

    Use this when:
    - Starting any new conversation (first thing to call)
    - Checking what's in progress: `my_sessions()`
    - Deciding whether to start a new session or resume an existing one

    Returns:
        A list of active sessions with IDs, descriptions, status, and
        last-updated timestamps. Returns an empty list if no active sessions.
        Completed sessions are not shown (they auto-expire after 48 hours).
    """
    return await _proxy("my_sessions")


@mcp.tool()
async def promote_session(session_id: str, key_takeaways: list[str]) -> str:
    """Save the most important things from a session as permanent memories.

    Session data expires 48 hours after completion. Use this to extract
    key learnings before ending a session — promoted items become
    permanent memories that persist forever.

    Use this when:
    - Before calling `end_session`: `promote_session("s001", ["OAuth2 migration requires updating all 3 microservices", "Rate limiter must fail closed for auth endpoints"])`
    - Important decisions were made during the session
    - You discovered patterns worth remembering long-term

    Args:
        session_id: The session to promote from (e.g., "s001"). Must be
            an active (not yet completed) session.
        key_takeaways: List of strings — each becomes a permanent memory.
            Be specific and include context so they're useful standalone.

    Returns:
        Count of how many takeaways were promoted to permanent memory.
        Returns an error if the session doesn't exist or key_takeaways is empty.
    """
    return await _proxy("promote_session", session_id=session_id, key_takeaways=key_takeaways)


# ── Notes ───────────────────────────────────────────────────────────

@mcp.tool()
async def save_note(name: str, content: str, session_id: Optional[str] = None) -> str:
    """Save a named note for later retrieval.

    Notes are stored by name and can be retrieved exactly with `get_note`.
    Unlike memories (which are searched by meaning), notes are accessed
    by their exact name — like files in a folder.

    Use this when:
    - Saving structured data: `save_note("api-endpoints", "GET /users, POST /auth, ...")`
    - Preserving analysis results: `save_note("perf-audit-2024", "P95 latency: 240ms...")`
    - Storing meeting notes: `save_note("standup-mar-15", "Discussed auth migration...")`
    - Attaching work to a session: `save_note("findings", "...", session_id="s001")`

    If a note with the same name already exists, it is overwritten.

    Args:
        name: A short, descriptive name (e.g., "api-auth-flow", "meeting-notes-q1").
            Use lowercase with hyphens for consistency.
        content: The note content. Markdown is supported. No size limit,
            but keep it focused — use multiple notes for different topics.
        session_id: Optional session to attach this note to. Notes attached
            to sessions appear when that session is resumed.

    Returns:
        Confirmation that the note was saved. Returns an error if name
        or content is empty.
    """
    return await _proxy("save_note", name=name, content=content, session_id=session_id)


@mcp.tool()
async def get_note(name: str, session_id: Optional[str] = None) -> str:
    """Retrieve a saved note by its exact name.

    Fetches the full content of a note previously created with `save_note`.
    The name must match exactly (case-sensitive).

    Use this when:
    - Retrieving stored data: `get_note("api-endpoints")`
    - Checking session-attached notes: `get_note("findings", session_id="s001")`
    - Loading a reference document you saved earlier

    If you're not sure of the note name, use `recall` to search by content
    or check session context with `resume_session`.

    Args:
        name: The exact note name used when saving (case-sensitive).
        session_id: Required if the note was saved with a session_id.
            Omit for notes saved without a session.

    Returns:
        The full note content. Returns an error if no note exists with
        that name, or if session_id is required but not provided.
    """
    return await _proxy("get_note", name=name, session_id=session_id)


# ── Onboarding ──────────────────────────────────────────────────────

@mcp.tool()
async def getting_started() -> str:
    """Get the complete Astria operating guide.

    Returns a comprehensive guide covering all available tools,
    recommended workflows, conventions, and best practices for
    working with persistent memory effectively.

    Use this when:
    - Connecting to Astria for the first time
    - You need a refresher on available capabilities
    - Onboarding a new AI platform to your memory

    Returns:
        The full Astria setup and usage guide as formatted text.
    """
    return await _proxy("getting_started")


# ── Proxy ───────────────────────────────────────────────────────────

async def _proxy(tool_name: str, **kwargs) -> str:
    """Proxy a tool call to the remote Astria instance."""
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    try:
        transport = SSETransport(sse_url, headers=headers)
        async with Client(transport) as client:
            result = await client.call_tool(tool_name, kwargs)
            # FastMCP 3.2: result is CallToolResult with .content list
            if hasattr(result, 'content'):
                parts = result.content
                if parts and len(parts) > 0:
                    return parts[0].text if hasattr(parts[0], 'text') else str(parts[0])
            # Fallback for older API
            if hasattr(result, 'text'):
                return result.text
            return str(result)
    except Exception as e:
        return f"Connection error: {e}. Verify your ASTRIA_ENDPOINT and ASTRIA_API_KEY."


if __name__ == "__main__":
    mcp.run()
