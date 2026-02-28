"""
NyayaSahaya — Legal issue classifier service.
"""

import json
import logging
from app.services.llm_service import LLMService
from app.services.language_service import LanguageService
from app.utils.constants import CLASSIFIER_PROMPT, LEGAL_CATEGORIES, DISCLAIMER

logger = logging.getLogger(__name__)


class ClassifierService:
    """Classifies legal issues into predefined categories using LLM."""

    def __init__(self):
        self.llm = LLMService()
        self.language = LanguageService()

    async def classify(self, description: str) -> dict:
        """
        Classify a legal issue description.
        Returns category, confidence, and explanation.
        """
        detected_lang = self.language.detect_language(description)

        # Translate to English for classification if Tamil
        classify_text = description
        if detected_lang == "ta":
            classify_text = await self.language.translate(description, "ta", "en")

        prompt = CLASSIFIER_PROMPT.format(description=classify_text)

        response = await self.llm.generate_json(
            system_prompt="You are a legal issue classifier for Indian law. Always respond with valid JSON.",
            user_prompt=prompt,
        )

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse classifier JSON: {response}")
            result = {
                "category": "Civil",
                "confidence": "Low",
                "explanation": "Could not parse classification result.",
            }

        # Validate category
        if result.get("category") not in LEGAL_CATEGORIES:
            result["category"] = "Civil"
            result["confidence"] = "Low"

        # Translate explanation back to Tamil if needed
        if detected_lang == "ta" and result.get("explanation"):
            result["explanation"] = await self.language.translate(
                result["explanation"], "en", "ta"
            )

        result["detected_language"] = detected_lang
        result["disclaimer"] = DISCLAIMER
        return result
