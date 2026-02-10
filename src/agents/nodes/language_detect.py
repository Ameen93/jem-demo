"""Language detection node for LangGraph."""

import logging

from src.agents.llm import get_llm
from src.agents.state import AgentState
from src.i18n.detector import detect_language as keyword_detect

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {"en", "zu", "xh", "af", "nso", "st"}


def _detect_language(text: str) -> str:
    """Detect language using keyword matching first, then Claude API fallback.

    Args:
        text: User message text.

    Returns:
        ISO 639-1 language code.
    """
    # Try keyword-based detection first (no API call needed)
    detected = keyword_detect(text)
    if detected != "en":
        return detected

    # Fall back to LLM for ambiguous cases
    llm = get_llm(max_tokens=10)
    response = llm.invoke(
        f"Detect the language of this text and respond with ONLY the ISO 639-1 "
        f"code (en, zu, xh, af, nso, st): \"{text}\""
    )
    code = response.content.strip().lower()
    if code in SUPPORTED_LANGUAGES:
        return code
    return "en"


def language_detect(state: AgentState) -> dict:
    """Detect language from the latest user message.

    Args:
        state: Current agent state.

    Returns:
        State update with detected language.
    """
    try:
        last_message = state["messages"][-1].content
        detected = _detect_language(last_message)
        logger.info("Detected language: %s", detected)
        return {"language": detected}
    except Exception:
        logger.exception("Language detection failed, defaulting to English")
        return {"language": "en"}
