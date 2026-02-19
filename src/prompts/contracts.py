from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Protocol

if TYPE_CHECKING:
    from src.prompts.registry import PromptConfig


class PromptProvider(Protocol):
    def get_prompt(self, name: str) -> str: ...

    def list_prompts(self) -> Dict[str, PromptConfig]: ...
