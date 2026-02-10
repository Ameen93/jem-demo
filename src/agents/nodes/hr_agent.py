"""HR agent node for LangGraph."""

import logging

from langchain_anthropic import ChatAnthropic

from src.agents.state import AgentState
from src.mcp_server.tools.hr_tools import (
    get_employee,
    get_leave_balance,
    get_payslip,
    submit_leave_request,
)

logger = logging.getLogger(__name__)


def _call_hr_tool(message: str, employee_id: str) -> dict:
    """Determine and call the appropriate HR tool.

    Args:
        message: User message.
        employee_id: Employee ID.

    Returns:
        Tool result dict.
    """
    llm = ChatAnthropic(model="claude-sonnet-4-5-20250929", max_tokens=20)
    response = llm.invoke(
        f"Which HR tool should be called? Respond with ONLY the tool name.\n"
        f"Tools: get_employee, get_leave_balance, get_payslip, submit_leave_request\n"
        f"Message: \"{message}\""
    )
    tool_name = response.content.strip().lower()

    if tool_name == "get_leave_balance":
        return get_leave_balance(employee_id)
    elif tool_name == "get_payslip":
        return get_payslip(employee_id, "2026-02")
    elif tool_name == "get_employee":
        return get_employee(employee_id)
    else:
        return get_leave_balance(employee_id)


def hr_agent(state: AgentState) -> dict:
    """Process HR queries by calling appropriate tools.

    Args:
        state: Current agent state.

    Returns:
        State update with tool_results.
    """
    try:
        message = state["messages"][-1].content
        employee_id = state["employee_id"]
        result = _call_hr_tool(message, employee_id)
        return {"tool_results": result}
    except Exception:
        logger.exception("HR agent error")
        return {"error": "Unable to process HR query"}
