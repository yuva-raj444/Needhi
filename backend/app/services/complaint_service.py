"""
NyayaSahaya — Legal complaint draft generation service.
"""

import logging
from app.services.llm_service import LLMService
from app.utils.constants import COMPLAINT_PROMPT_EN, COMPLAINT_PROMPT_TA, DISCLAIMER

logger = logging.getLogger(__name__)


class ComplaintService:
    """Generate formal legal complaint drafts using LLM."""

    def __init__(self):
        self.llm = LLMService()

    async def generate_complaint(
        self,
        complainant_name: str,
        complainant_address: str,
        opponent_name: str,
        issue_description: str,
        location: str,
        date: str,
        language: str = "en",
    ) -> dict:
        """Generate a formal legal complaint letter."""

        template = COMPLAINT_PROMPT_EN if language == "en" else COMPLAINT_PROMPT_TA

        prompt = template.format(
            complainant_name=complainant_name,
            complainant_address=complainant_address,
            opponent_name=opponent_name,
            issue_description=issue_description,
            location=location,
            date=date,
        )

        system_msg = (
            "You are an expert Indian legal document drafter. "
            "Generate formal, properly formatted legal complaint letters."
        )

        draft = await self.llm.generate(
            system_prompt=system_msg,
            user_prompt=prompt,
            temperature=0.3,
            max_tokens=2500,
        )

        return {
            "draft_text": draft,
            "language": language,
            "disclaimer": DISCLAIMER,
        }
