"""Internationalization module for Jem HR Demo."""

from .detector import detect_language, iso_to_nllb
from .translator import get_translator, translate

__all__ = [
    "detect_language",
    "get_translator",
    "iso_to_nllb",
    "translate",
]
