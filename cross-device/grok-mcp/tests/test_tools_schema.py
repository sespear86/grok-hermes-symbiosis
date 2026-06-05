"""Ensure FastMCP registers five grok_* tools."""

from grok_mcp.server import mcp


def test_tool_names_registered() -> None:
    tools = mcp._tool_manager.list_tools()
    names = {t.name for t in tools}
    expected = {
        "grok_implement",
        "grok_design",
        "grok_check",
        "grok_review",
        "grok_best_of_n",
    }
    assert expected <= names