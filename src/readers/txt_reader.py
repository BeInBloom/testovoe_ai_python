from pathlib import Path
from typing import List, Optional
from src.domain.models import ContentType, DocumentContent

class TxtReader:
    def __init__(self, supported_extensions: Optional[List[str]] = None):
        self._supported_extensions = supported_extensions or [".txt", ".md", ".markdown"]

    def supports(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self._supported_extensions

    def read(self, file_path: Path) -> DocumentContent:
        content = self._read_file(file_path)
        
        return DocumentContent(
            file_path=file_path,
            content_type=ContentType.TEXT,
            text_content=content,
        )

    def _read_file(self, file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def get_supported_extensions(self) -> List[str]:
        return self._supported_extensions
