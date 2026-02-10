"""Tests for i18n module: NLLB translation and language detection (Stories 7.1-7.3)."""

from unittest.mock import MagicMock, patch


class TestTranslatorLoading:
    """Tests for NLLB model loading (Story 7.1)."""

    def test_translator_initializes(self):
        """Translator module can be imported and initialized."""
        from src.i18n.translator import get_translator

        translator = get_translator()
        assert translator is not None

    @patch("src.i18n.translator._load_model")
    def test_fallback_on_load_failure(self, mock_load):
        """Falls back gracefully if model loading fails."""
        from src.i18n.translator import translate

        mock_load.side_effect = Exception("Model not found")
        result = translate("Hello, how are you?", "eng_Latn", "zul_Latn")
        # Fallback: return original text
        assert result == "Hello, how are you?"

    def test_english_passthrough(self):
        """English to English returns text unchanged."""
        from src.i18n.translator import translate

        result = translate("Hello", "eng_Latn", "eng_Latn")
        assert result == "Hello"


class TestLanguageDetection:
    """Tests for language detection enhancement (Story 7.2)."""

    def test_detect_english(self):
        """English text detected correctly."""
        from src.i18n.detector import detect_language

        result = detect_language("How many leave days do I have?")
        assert result == "en"

    def test_detect_zulu_keywords(self):
        """isiZulu text detected via keyword matching."""
        from src.i18n.detector import detect_language

        result = detect_language("Sawubona, ngicela ukubona imali yami")
        assert result == "zu"

    def test_detect_afrikaans_keywords(self):
        """Afrikaans text detected via keyword matching."""
        from src.i18n.detector import detect_language

        result = detect_language("Hoeveel verlof het ek oor?")
        assert result == "af"

    def test_detect_xhosa_keywords(self):
        """isiXhosa text detected via keyword matching."""
        from src.i18n.detector import detect_language

        result = detect_language("Molo, ndifuna ukwazi ngemali yam")
        assert result == "xh"

    def test_fallback_to_english(self):
        """Unknown text defaults to English."""
        from src.i18n.detector import detect_language

        result = detect_language("12345")
        assert result == "en"

    def test_nllb_code_mapping(self):
        """ISO codes map to NLLB codes correctly."""
        from src.i18n.detector import iso_to_nllb

        assert iso_to_nllb("en") == "eng_Latn"
        assert iso_to_nllb("zu") == "zul_Latn"
        assert iso_to_nllb("xh") == "xho_Latn"
        assert iso_to_nllb("af") == "afr_Latn"
        assert iso_to_nllb("nso") == "nso_Latn"
        assert iso_to_nllb("st") == "sot_Latn"


class TestTranslation:
    """Tests for response translation (Story 7.3)."""

    @patch("src.i18n.translator._get_pipeline")
    def test_translation_called(self, mock_pipeline):
        """Translation pipeline is called for non-English targets."""
        from src.i18n.translator import translate

        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"translation_text": "Sawubona"}]
        mock_pipeline.return_value = mock_pipe

        result = translate("Hello", "eng_Latn", "zul_Latn")
        assert result == "Sawubona"
        mock_pipe.assert_called_once()

    @patch("src.i18n.translator._get_pipeline")
    def test_translation_failure_returns_original(self, mock_pipeline):
        """Translation failure returns original English text."""
        from src.i18n.translator import translate

        mock_pipeline.side_effect = Exception("Translation failed")
        result = translate("Hello", "eng_Latn", "zul_Latn")
        assert result == "Hello"
