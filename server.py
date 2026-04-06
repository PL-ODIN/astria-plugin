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

    Anything you save here persists forever and can be found later
    by searching for its meaning — not just exact words.

    Args:
        content: What to remember — facts, decisions, preferences, anything
        category: Optional tag (preference, fact, decision, idea, project)
        importance: low, normal, or high — high surfaces first
    """
    return await _proxy("remember", content=content, category=category, importance=importance)


@mcp.tool()
async def recall(query: str, limit: int = 5, category: Optional[str] = None) -> str:
    """Search your memories by meaning.

    Finds the most relevant things you've saved, ranked by how
    closely they match what you're looking for.

    Args:
        query: What you're looking for (natural language)
        limit: How many results (default 5, max 20)
        category: Filter to a category
    """
    return await _proxy("recall", query=query, limit=limit, category=category)


@mcp.tool()
async def forget(memory_id: str) -> str:
    """Remove a specific memory permanently.

    Args:
        memory_id: Memory ID from remember or recall results
    """
    return await _proxy("forget", memory_id=memory_id)


@mcp.tool()
async def list_memories(category: Optional[str] = None, limit: int = 20) -> str:
    """Browse your stored memories, most recent first.

    Args:
        category: Filter by category (optional)
        limit: How many (default 20, max 100)
    """
    return await _proxy("list_memories", category=category, limit=limit)


# ── Reflect ─────────────────────────────────────────────────────────

@mcp.tool()
async def my_memory_stats() -> str:
    """See an overview of your memory network.

    Shows how many memories you have, broken down by category,
    active sessions, saved notes, and learned insights.
    """
    return await _proxy("my_memory_stats")


# ── Insights ────────────────────────────────────────────────────────

@mcp.tool()
async def record_insight(pattern: str, cause: str, solution: str, confidence: float = 0.7) -> str:
    """Record a cause-and-effect pattern you've discovered.

    Over time, your memory builds a library of insights that surface
    automatically when similar situations come up again.

    Args:
        pattern: What you observed (e.g., "deploys fail on Fridays")
        cause: Why it happens (e.g., "cache expires weekly")
        solution: How to fix it (e.g., "flush cache before Friday deploys")
        confidence: How sure you are (0.0 to 1.0)
    """
    return await _proxy("record_insight", pattern=pattern, cause=cause, solution=solution, confidence=confidence)


@mcp.tool()
async def my_insights(limit: int = 20) -> str:
    """Browse your discovered patterns and insights.

    Shows cause-and-effect patterns ranked by how often
    they've been observed.

    Args:
        limit: How many (default 20, max 50)
    """
    return await _proxy("my_insights", limit=limit)


# ── Sessions ────────────────────────────────────────────────────────

@mcp.tool()
async def start_session(description: str) -> str:
    """Start a working session for cross-conversation continuity.

    Sessions let you pick up exactly where you left off, even
    in a completely new conversation.

    Args:
        description: What you're working on
    """
    return await _proxy("start_session", description=description)


@mcp.tool()
async def resume_session(session_id: str) -> str:
    """Resume a previous session — get full context to continue.

    Args:
        session_id: Session ID (e.g., "s001")
    """
    return await _proxy("resume_session", session_id=session_id)


@mcp.tool()
async def end_session(session_id: str, summary: Optional[str] = None) -> str:
    """End a session and save what was accomplished.

    Args:
        session_id: Session to complete
        summary: Brief summary of the outcome
    """
    return await _proxy("end_session", session_id=session_id, summary=summary)


@mcp.tool()
async def my_sessions() -> str:
    """List active sessions you can resume."""
    return await _proxy("my_sessions")


@mcp.tool()
async def promote_session(session_id: str, key_takeaways: list[str]) -> str:
    """Save the most important things from a session as permanent memories.

    Use this when ending a session to make sure key learnings are
    remembered forever, not just for the session's lifetime.

    Args:
        session_id: The session these came from
        key_takeaways: List of important things to save permanently
    """
    return await _proxy("promote_session", session_id=session_id, key_takeaways=key_takeaways)


# ── Notes ───────────────────────────────────────────────────────────

@mcp.tool()
async def save_note(name: str, content: str, session_id: Optional[str] = None) -> str:
    """Save a named note for later retrieval.

    Give it a name, get it back anytime. Good for analysis results,
    meeting notes, drafts, or any data you want to access by name.

    Args:
        name: Name for this note (e.g., "meeting-notes", "budget-v2")
        content: The content to save
        session_id: Optional session to attach it to
    """
    return await _proxy("save_note", name=name, content=content, session_id=session_id)


@mcp.tool()
async def get_note(name: str, session_id: Optional[str] = None) -> str:
    """Retrieve a saved note by name.

    Args:
        name: Note name
        session_id: If saved to a session
    """
    return await _proxy("get_note", name=name, session_id=session_id)


# ── Onboarding ──────────────────────────────────────────────────────

@mcp.tool()
async def getting_started() -> str:
    """Get the Astria operating guide.

    Call this the first time you connect to learn how to use
    Astria's memory tools effectively.
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
            if result and len(result) > 0:
                return result[0].text if hasattr(result[0], 'text') else str(result[0])
            return str(result)
    except Exception as e:
        return f"Connection error: {e}. Verify your ASTRIA_ENDPOINT and ASTRIA_API_KEY."


if __name__ == "__main__":
    mcp.run()
