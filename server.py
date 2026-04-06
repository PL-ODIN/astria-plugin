"""Astria MCP Server — thin proxy to your dedicated Astria instance.

Connects to your Astria memory infrastructure via SSE and exposes
all tools locally. Used by Glama for inspection and by MCP clients
that prefer local stdio transport.
"""

import os
import sys

from fastmcp import Client, FastMCP
from fastmcp.client.transports import SSETransport

ENDPOINT = os.environ.get("ASTRIA_ENDPOINT", "")
API_KEY = os.environ.get("ASTRIA_API_KEY", "")

if not ENDPOINT:
    print("ASTRIA_ENDPOINT is required. Get yours at https://astriaindex.com/dashboard", file=sys.stderr)
    sys.exit(1)

# Ensure endpoint ends with /sse
sse_url = ENDPOINT.rstrip("/")
if not sse_url.endswith("/sse"):
    sse_url += "/sse"

mcp = FastMCP(
    "Astria",
    description="Persistent AI memory — neural pathway architecture for cross-session recall, contextual awareness, and memory promotion.",
)


# Define all 14 Astria tools with their schemas for inspection.
# When called, these proxy to the remote Astria instance.

@mcp.tool()
async def remember(content: str, category: str = "general", importance: str = "medium") -> str:
    """Save a memory to your persistent knowledge graph.

    Stores facts, decisions, preferences, ideas, projects, and insights
    with semantic embeddings for natural language recall.

    Args:
        content: What to remember (fact, decision, preference, idea, project context)
        category: One of: fact, decision, preference, idea, project, person, general
        importance: Priority level: low, medium, high (high = always surfaces in recall)
    """
    return await _proxy("remember", content=content, category=category, importance=importance)


@mcp.tool()
async def recall(query: str, limit: int = 5) -> str:
    """Search your memory using natural language.

    Finds relevant memories by meaning, not just keywords. Returns matches
    ranked by semantic similarity with full context.

    Args:
        query: Natural language search (e.g., "what database did we choose?")
        limit: Max results to return (default 5)
    """
    return await _proxy("recall", query=query, limit=limit)


@mcp.tool()
async def forget(memory_id: str) -> str:
    """Remove a memory from your knowledge graph.

    Args:
        memory_id: The ID of the memory to forget
    """
    return await _proxy("forget", memory_id=memory_id)


@mcp.tool()
async def start_session(request: str, plan: str = "") -> str:
    """Start a new working session for cross-conversation continuity.

    Sessions track your work across multiple conversations. Start one for
    any task that spans more than a single chat.

    Args:
        request: What you're working on (stored verbatim)
        plan: Optional execution plan
    """
    return await _proxy("start_session", request=request, plan=plan)


@mcp.tool()
async def my_sessions() -> str:
    """List all active sessions. Call this at the start of every conversation
    to check for interrupted work that should be resumed."""
    return await _proxy("my_sessions")


@mcp.tool()
async def end_session(session_id: str, summary: str = "") -> str:
    """End a working session with an optional summary.

    Args:
        session_id: The session to close
        summary: Final summary of what was accomplished
    """
    return await _proxy("end_session", session_id=session_id, summary=summary)


@mcp.tool()
async def save_note(name: str, content: str) -> str:
    """Save a structured note with a name for easy retrieval.

    Use for: meeting notes, API docs, configuration references,
    code snippets, analysis results.

    Args:
        name: Note title (e.g., "api-auth-flow", "meeting-2024-03-15")
        content: The note content (markdown supported)
    """
    return await _proxy("save_note", name=name, content=content)


@mcp.tool()
async def get_note(name: str) -> str:
    """Retrieve a saved note by name.

    Args:
        name: The note title to retrieve
    """
    return await _proxy("get_note", name=name)


@mcp.tool()
async def record_insight(pattern: str, cause: str, resolution: str) -> str:
    """Record a cause-and-effect pattern you've discovered.

    Insights are the deepest memory tier — understanding WHY things happen.
    They guide future analysis: "I've seen this before."

    Args:
        pattern: The observable symptom or pattern
        cause: The root cause
        resolution: How to fix or handle it
    """
    return await _proxy("record_insight", pattern=pattern, cause=cause, resolution=resolution)


@mcp.tool()
async def promote_session(session_id: str) -> str:
    """Promote key learnings from a session into permanent memory.

    Extracts important facts, decisions, and patterns from the session
    and saves them as standalone memories that persist forever.

    Args:
        session_id: The session to promote learnings from
    """
    return await _proxy("promote_session", session_id=session_id)


@mcp.tool()
async def memory_stats() -> str:
    """View your memory statistics — total memories, categories, sessions,
    notes, insights, and embeddings."""
    return await _proxy("memory_stats")


@mcp.tool()
async def search_memories(query: str, category: str = "", limit: int = 10) -> str:
    """Advanced memory search with optional category filter.

    Args:
        query: Natural language search query
        category: Optional filter: fact, decision, preference, idea, project, person
        limit: Max results (default 10)
    """
    return await _proxy("search_memories", query=query, category=category, limit=limit)


@mcp.tool()
async def list_notes() -> str:
    """List all saved notes with their names and creation dates."""
    return await _proxy("list_notes")


@mcp.tool()
async def first_time_setup(ai_platform: str = "", project_description: str = "") -> str:
    """First-time onboarding — get the complete operating guide, available
    capabilities, tool reference, and check for interrupted work.

    Args:
        ai_platform: Which AI platform is connecting (claude_code, cursor, etc.)
        project_description: Brief description of your project
    """
    return await _proxy("first_time_setup", ai_platform=ai_platform, project_description=project_description)


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
