"""LangGraph agent state definition."""

from typing import Optional

from langchain_core.messages import BaseMessage, HumanMessage
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State that flows through the LangGraph agent graph."""

    messages: list[BaseMessage]
    language: str
    employee_id: Optional[str]
    employee: Optional[dict]
    intent: str
    tool_results: dict
    response: str
    error: Optional[str]


def create_initial_state(employee_id: str, message: str) -> AgentState:
    """Create an initial agent state.

    Args:
        employee_id: The employee ID for context.
        message: The user's message.

    Returns:
        Initialized AgentState.
    """
    return AgentState(
        messages=[HumanMessage(content=message)],
        language="en",
        employee_id=employee_id,
        employee=None,
        intent="",
        tool_results={},
        response="",
        error=None,
    )
