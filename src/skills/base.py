from typing import Protocol, Any, Dict
from pathlib import Path


class Skill(Protocol):
    name: str
    description: str

    def execute(self, context: Dict[str, Any]) -> Any: ...
