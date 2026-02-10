"""Intent classification and routing node for LangGraph."""

import logging

from langchain_anthropic import ChatAnthropic

from src.agents.state import AgentState

logger = logging.getLogger(__name__)

VALID_INTENTS = {"hr_query", "ewa_request", "policy_question"}


def _classify_intent(text: str) -> str:
    """Classify user intent using Claude API.

    Args:
        text: User message text.

    Returns:
        One of: hr_query, ewa_request, policy_question.
    """
    llm = ChatAnthropic(model="claude-sonnet-4-5-20250929", max_tokens=20)
    response = llm.invoke(
        f"Classify this HR employee message into exactly one category. "
        f"Respond with ONLY the category name.\n"
        f"Categories:\n"
        f"- hr_query: leave balance, payslip, employee info, time off requests\n"
        f"- ewa_request: earned wage access, salary advance, early pay\n"
        f"- policy_question: company policy, rules, regulations, entitlements\n\n"
        f"Message: \"{text}\""
    )
    intent = response.content.strip().lower()
    if intent in VALID_INTENTS:
        return intent
    return "hr_query"


def intent_router(state: AgentState) -> dict:
    """Classify intent from the latest user message.

    Args:
        state: Current agent state.

    Returns:
        State update with classified intent.
    """
    try:
        last_message = state["messages"][-1].content
        intent = _classify_intent(last_message)
        logger.info("Classified intent: %s", intent)
        return {"intent": intent}
    except Exception:
        logger.exception("Intent classification failed, defaulting to hr_query")
        return {"intent": "hr_query"}


def route_by_intent(state: AgentState) -> str:
    """Route to the appropriate agent based on intent.

    Args:
        state: Current agent state.

    Returns:
        Node name to route to.
    """
    intent = state.get("intent", "hr_query")
    routes = {
        "hr_query": "hr_agent",
        "ewa_request": "ewa_agent",
        "policy_question": "policy_rag",
    }
    return routes.get(intent, "hr_agent")
