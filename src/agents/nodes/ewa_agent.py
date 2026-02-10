"""EWA agent node for LangGraph."""

import logging

from src.agents.llm import get_llm
from src.agents.state import AgentState
from src.mcp_server.tools.ewa_tools import check_ewa_eligibility, request_ewa_advance

logger = logging.getLogger(__name__)


def _call_ewa_tool(message: str, employee_id: str) -> dict:
    """Determine and call the appropriate EWA tool.

    Args:
        message: User message.
        employee_id: Employee ID.

    Returns:
        Tool result dict.
    """
    llm = get_llm(max_tokens=20)
    response = llm.invoke(
        f"Does this message request an EWA advance or just check eligibility? "
        f"Respond with ONLY: 'check' or 'request'\n"
        f"Message: \"{message}\""
    )
    action = response.content.strip().lower()

    if "request" in action:
        # Check eligibility first to get available amount
        eligibility = check_ewa_eligibility(employee_id)
        if eligibility["success"] and eligibility["data"].get("eligible"):
            available = eligibility["data"]["available"]
            # Default to available amount if no specific amount mentioned
            return request_ewa_advance(employee_id, min(available, 1500))
        return eligibility
    else:
        return check_ewa_eligibility(employee_id)


def ewa_agent(state: AgentState) -> dict:
    """Process EWA requests by calling appropriate tools.

    Args:
        state: Current agent state.

    Returns:
        State update with tool_results.
    """
    try:
        message = state["messages"][-1].content
        employee_id = state["employee_id"]
        result = _call_ewa_tool(message, employee_id)
        return {"tool_results": result}
    except Exception:
        logger.exception("EWA agent error")
        return {"error": "Unable to process EWA request"}
