"""Response formatting node for LangGraph."""

import json
import logging

from src.agents.llm import get_llm
from src.agents.state import AgentState
from src.i18n.detector import iso_to_nllb
from src.i18n.translator import translate

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
    llm = get_llm(max_tokens=500)
    response = llm.invoke(
        f"Generate a helpful, concise response to the employee's question "
        f"based on these tool results. Respond in English.\n\n"
        f"Rules:\n"
        f"- For leave submissions: say the request has been submitted and will be sent to their manager for approval. Never say it IS approved.\n"
        f"- For balances: state the exact numbers from the data.\n"
        f"- Be factual — only state what the data shows, do not speculate.\n\n"
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

        # Translate to user's language if not English
        if language != "en":
            nllb_target = iso_to_nllb(language)
            formatted = translate(formatted, "eng_Latn", nllb_target)

        return {"response": formatted}
    except Exception:
        logger.exception("Response formatting error")
        return {"response": "I'm sorry, I was unable to process your request."}
