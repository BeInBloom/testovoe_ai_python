from pathlib import Path
from typing import List, Optional

import pdfplumber

from src.domain.models import ContentType, DocumentContent


class PdfReader:
    _MIME_TYPE: str = "application/pdf"

    def __init__(self, supported_extensions: Optional[List[str]] = None):
        self._supported_extensions = supported_extensions or [".pdf"]

    def supports(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self._supported_extensions

    def read(self, file_path: Path) -> DocumentContent:
        text_content = self._extract_text_from_pdf(file_path)

        return DocumentContent(
            file_path=file_path,
            content_type=ContentType.TEXT,
            text_content=text_content,
            mime_type="text/plain",
        )

    def _extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF using pdfplumber."""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except Exception as e:
            return f"Error extracting text from PDF {file_path.name}: {str(e)}"

    def get_supported_extensions(self) -> List[str]:
        return self._supported_extensions
