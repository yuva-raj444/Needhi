"""
NyayaSahaya — Language detection and translation service.
"""

import logging
from langdetect import detect, LangDetectException
from app.services.llm_service import LLMService
from app.utils.constants import TRANSLATION_PROMPT

logger = logging.getLogger(__name__)


class LanguageService:
    """Detect input language and translate responses."""

    def __init__(self):
        self.llm = LLMService()

    def detect_language(self, text: str) -> str:
        """
        Detect whether input is Tamil or English.
        Returns 'ta' or 'en'.
        """
        try:
            lang = detect(text)
            if lang == "ta":
                return "ta"
            return "en"
        except LangDetectException:
            return "en"

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text between Tamil and English using the LLM."""
        lang_names = {"en": "English", "ta": "Tamil"}
        prompt = TRANSLATION_PROMPT.format(
            source_lang=lang_names.get(source_lang, "English"),
            target_lang=lang_names.get(target_lang, "Tamil"),
            text=text,
        )
        return await self.llm.generate(
            system_prompt="You are a professional Tamil-English legal translator.",
            user_prompt=prompt,
            temperature=0.2,
        )
