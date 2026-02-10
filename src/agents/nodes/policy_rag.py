"""Policy RAG agent node for LangGraph."""

import logging

from src.agents.state import AgentState
from src.mcp_server.tools.policy_tools import search_policies

logger = logging.getLogger(__name__)


def policy_rag(state: AgentState) -> dict:
    """Retrieve policy information for user query.

    Args:
        state: Current agent state.

    Returns:
        State update with tool_results containing policy chunks.
    """
    try:
        query = state["messages"][-1].content
        result = search_policies(query)
        return {"tool_results": result}
    except Exception:
        logger.exception("Policy RAG error")
        return {"error": "Unable to retrieve policy information"}
