from typing import List

from src.core.logger import Logger
from src.domain.models import Document
from src.llm.contracts import LLMProvider


class SummaryGenerator:
    def __init__(self, llm_provider: LLMProvider, logger: Logger):
        self._llm_provider = llm_provider
        self._logger = logger

    def generate(self, documents: List[Document], prompt: str) -> str:
        if not documents:
            return "No documents to summarize."

        self._logger.info(f"Generating summary for {len(documents)} documents")

        summary = self._llm_provider.generate_summary(documents, prompt)

        self._logger.info("Summary generated successfully")

        return summary
