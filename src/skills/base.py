from typing import Any, Dict, Protocol


class Skill(Protocol):
    name: str
    description: str

    def execute(self, context: Dict[str, Any]) -> Any: ...
