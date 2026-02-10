"""NLLB-200 translation for South African languages."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

_pipeline: Any = None
_model_loaded = False
_load_attempted = False

MODEL_NAME = "facebook/nllb-200-distilled-600M"


def _load_model() -> Any:
    """Load the NLLB translation model.

    Returns:
        HuggingFace translation pipeline.

    Raises:
        Exception: If model loading fails.
    """
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

    logger.info("Loading NLLB model: %s", MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    pipe = pipeline("translation", model=model, tokenizer=tokenizer, max_length=512)
    logger.info("NLLB model loaded successfully")
    return pipe


def _get_pipeline() -> Any:
    """Get the translation pipeline, loading if needed (lazy loading).

    Returns:
        Translation pipeline or None if loading failed.
    """
    global _pipeline, _model_loaded, _load_attempted

    if _model_loaded:
        return _pipeline

    if _load_attempted:
        return None

    _load_attempted = True
    try:
        _pipeline = _load_model()
        _model_loaded = True
        return _pipeline
    except Exception:
        logger.warning("NLLB model loading failed, falling back to English-only mode")
        return None


def get_translator() -> dict:
    """Get translator status information.

    Returns:
        Dict with model status.
    """
    return {
        "model": MODEL_NAME,
        "loaded": _model_loaded,
        "attempted": _load_attempted,
    }


def translate(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text between languages using NLLB-200.

    Args:
        text: Text to translate.
        source_lang: Source NLLB language code (e.g., 'eng_Latn').
        target_lang: Target NLLB language code (e.g., 'zul_Latn').

    Returns:
        Translated text, or original text on failure/passthrough.
    """
    if source_lang == target_lang:
        return text

    try:
        pipe = _get_pipeline()
        if pipe is None:
            logger.debug("No translation pipeline available, returning original text")
            return text

        result = pipe(text, src_lang=source_lang, tgt_lang=target_lang)
        translated = result[0]["translation_text"]
        logger.debug("Translated: '%s' -> '%s'", text[:50], translated[:50])
        return translated
    except Exception:
        logger.warning("Translation failed, returning original text")
        return text
