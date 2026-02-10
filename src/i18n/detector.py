"""Language detection for South African languages."""

import logging
import re

logger = logging.getLogger(__name__)

# Keyword-based detection for SA languages
_LANGUAGE_KEYWORDS = {
    "zu": [
        "sawubona", "ngicela", "ngifuna", "imali", "yami", "ukubona",
        "usuku", "amalanga", "umsebenzi", "ngiyabonga", "isikhathi",
        "ngiyanicela", "ngingathanda", "eholidini", "umholo",
    ],
    "xh": [
        "molo", "ndifuna", "ndingathanda", "imali", "yam", "ukwazi",
        "ndicela", "ndibona", "umsebenzi", "enkosi", "ixesha",
        "amalanga", "eholide", "umvuzo",
    ],
    "af": [
        "hoeveel", "verlof", "salaris", "asseblief", "dankie", "werk",
        "betaling", "geld", "voorskot", "beleid", "siekteverlof",
        "jaarlikse", "balans", "oor",
    ],
    "nso": [
        "dumela", "kgopela", "nyaka", "tshelete", "mosomo", "matšatši",
        "leholetse", "moputso", "lebaka",
    ],
    "st": [
        "lumela", "kopa", "batla", "tjhelete", "mosebetsi", "matsatsi",
        "phomolo", "moputso", "molao",
    ],
}

# ISO 639-1 to NLLB-200 language codes
_ISO_TO_NLLB = {
    "en": "eng_Latn",
    "zu": "zul_Latn",
    "xh": "xho_Latn",
    "af": "afr_Latn",
    "nso": "nso_Latn",
    "st": "sot_Latn",
}


def iso_to_nllb(iso_code: str) -> str:
    """Convert ISO 639-1 code to NLLB-200 language code."""
    return _ISO_TO_NLLB.get(iso_code, "eng_Latn")


def detect_language(text: str) -> str:
    """Detect language from text using keyword matching.

    Args:
        text: User message text.

    Returns:
        ISO 639-1 language code (en, zu, xh, af, nso, st).
    """
    words = set(re.findall(r"[a-zšž]+", text.lower()))
    scores: dict[str, int] = {}

    for lang, keywords in _LANGUAGE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in words)
        if score > 0:
            scores[lang] = score

    if scores:
        best = max(scores, key=scores.get)
        logger.debug("Language detected: %s (score: %d)", best, scores[best])
        return best

    return "en"
