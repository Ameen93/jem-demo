"""Response formatting node for LangGraph."""

import json
import logging

from langchain_anthropic import ChatAnthropic

from src.agents.state import AgentState

logger = logging.getLogger(__name__)


def _format_response(tool_results: dict, language: str, query: str) -> str:
    """Format tool results into a natural language response.

    Args:
        tool_results: Results from tool execution.
        language: Detected language code.
        query: Original user query.

    Returns:
        Formatted natural language response.
    """
    llm = ChatAnthropic(model="claude-sonnet-4-5-20250929", max_tokens=500)
    response = llm.invoke(
        f"Generate a helpful, concise response to the employee's question "
        f"based on these tool results. Respond in English.\n\n"
        f"Employee question: {query}\n"
        f"Tool results: {json.dumps(tool_results)}\n\n"
        f"Response:"
    )
    return response.content.strip()


def response_format(state: AgentState) -> dict:
    """Format tool results into a natural language response.

    Args:
        state: Current agent state.

    Returns:
        State update with formatted response.
    """
    try:
        if state.get("error"):
            return {"response": f"I'm sorry, I encountered an error: {state['error']}"}

        tool_results = state.get("tool_results", {})
        language = state.get("language", "en")
        query = state["messages"][-1].content

        formatted = _format_response(tool_results, language, query)
        return {"response": formatted}
    except Exception:
        logger.exception("Response formatting error")
        return {"response": "I'm sorry, I was unable to process your request."}
