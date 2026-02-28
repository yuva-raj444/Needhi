"""
NyayaSahaya — Google Gemini LLM wrapper service.
Uses the new google-genai SDK.
"""

import logging
from google import genai
from google.genai import types
from app.config import get_settings

logger = logging.getLogger(__name__)


class LLMService:
    """Thin wrapper around the Google Gemini API."""

    def __init__(self):
        settings = get_settings()
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1500,
    ) -> str:
        """Send a generation request and return the text response."""
        try:
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            raise RuntimeError(f"LLM service error: {e}")

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
    ) -> str:
        """Generate a response expected to be JSON."""
        try:
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=800,
                    response_mime_type="application/json",
                ),
            )
            text = response.text.strip()
            # Strip markdown code fences if Gemini wraps them
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return text.strip()
        except Exception as e:
            logger.error(f"LLM JSON generation error: {e}")
            raise RuntimeError(f"LLM service error: {e}")
