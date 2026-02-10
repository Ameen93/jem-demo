"""LangGraph agent graph definition."""

import logging

from langgraph.graph import END, StateGraph

from .nodes import (
    ewa_agent,
    hr_agent,
    intent_router,
    language_detect,
    policy_rag,
    response_format,
    route_by_intent,
)
from .state import AgentState

logger = logging.getLogger(__name__)


def build_graph() -> StateGraph:
    """Build and compile the LangGraph agent graph.

    Returns:
        Compiled StateGraph.
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("language_detect", language_detect)
    graph.add_node("intent_router", intent_router)
    graph.add_node("hr_agent", hr_agent)
    graph.add_node("ewa_agent", ewa_agent)
    graph.add_node("policy_rag", policy_rag)
    graph.add_node("response_format", response_format)

    # Set entry point
    graph.set_entry_point("language_detect")

    # Add edges
    graph.add_edge("language_detect", "intent_router")
    graph.add_conditional_edges("intent_router", route_by_intent)
    graph.add_edge("hr_agent", "response_format")
    graph.add_edge("ewa_agent", "response_format")
    graph.add_edge("policy_rag", "response_format")
    graph.add_edge("response_format", END)

    return graph.compile()
