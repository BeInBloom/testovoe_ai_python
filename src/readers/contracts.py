from pathlib import Path
from typing import Protocol

from src.domain.models import DocumentContent


class DocumentReader(Protocol):
    def supports(self, file_path: Path) -> bool: ...
    def read(self, file_path: Path) -> DocumentContent: ...
    def get_supported_extensions(self) -> list[str]: ...
