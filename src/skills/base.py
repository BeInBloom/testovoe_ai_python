from typing import Any, Protocol


class Skill(Protocol):
    name: str
    description: str

    def execute(self, context: dict[str, Any]) -> Any: ...
