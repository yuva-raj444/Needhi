"""
NyayaSahaya — RAG (Retrieval-Augmented Generation) pipeline service.
"""

import logging
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService
from app.services.language_service import LanguageService
from app.utils.constants import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT, DISCLAIMER
from app.config import get_settings

logger = logging.getLogger(__name__)


class RAGService:
    """End-to-end RAG pipeline: retrieve → augment → generate."""

    def __init__(self):
        self.llm = LLMService()
        self.embeddings = EmbeddingService()
        self.language = LanguageService()
        self.settings = get_settings()

    async def answer_question(self, question: str, force_language: str | None = None) -> dict:
        """
        Full RAG flow:
        1. Detect language
        2. If Tamil, translate query to English for retrieval
        3. Search FAISS for relevant chunks
        4. Generate answer via LLM with context
        5. If original language was Tamil, instruct LLM to respond in Tamil
        """
        # 1 ─ Language detection
        detected_lang = force_language or self.language.detect_language(question)

        # 2 ─ Prepare English query for retrieval
        retrieval_query = question
        if detected_lang == "ta":
            retrieval_query = await self.language.translate(question, "ta", "en")

        # 3 ─ Retrieve relevant chunks
        top_k = self.settings.top_k_results
        results = self.embeddings.search(retrieval_query, top_k=top_k)

        if not results:
            no_data_msg = (
                "I don't have enough legal documents indexed yet to answer your question. "
                "Please upload relevant Indian law documents first."
            )
            if detected_lang == "ta":
                no_data_msg = await self.language.translate(no_data_msg, "en", "ta")
            return {
                "answer": no_data_msg,
                "detected_language": detected_lang,
                "sources": [],
                "disclaimer": DISCLAIMER,
            }

        # 4 ─ Build context from retrieved chunks
        context_parts = []
        sources = []
        for r in results:
            context_parts.append(f"[Source: {r.get('source', 'Unknown')}]\n{r['text']}")
            sources.append({
                "text": r["text"][:300] + ("..." if len(r["text"]) > 300 else ""),
                "source": r.get("source", "Unknown"),
                "score": r.get("score"),
            })

        context = "\n\n---\n\n".join(context_parts)

        # 5 ─ Construct prompts
        lang_instruction = ""
        if detected_lang == "ta":
            lang_instruction = "\n\nIMPORTANT: The user asked in Tamil. You MUST respond entirely in Tamil."

        system_prompt = RAG_SYSTEM_PROMPT.format(context=context) + lang_instruction
        user_prompt = RAG_USER_PROMPT.format(question=question)

        # 6 ─ Generate answer
        answer = await self.llm.generate(system_prompt, user_prompt)

        return {
            "answer": answer,
            "detected_language": detected_lang,
            "sources": sources,
            "disclaimer": DISCLAIMER,
        }
