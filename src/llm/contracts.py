from typing import Literal, Protocol

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str | list[dict]  # Поддержка мультимодальности


class LLMProvider(Protocol):
    def supports_multimodal(self) -> bool: ...
    def generate_response(self, messages: list[Message]) -> str: ...
