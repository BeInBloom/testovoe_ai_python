from typing import List, Protocol

from src.domain.models import Document


class LLMProvider(Protocol):
    def supports_multimodal(self) -> bool: ...
    def generate_summary(self, documents: List[Document], prompt: str) -> str: ...
