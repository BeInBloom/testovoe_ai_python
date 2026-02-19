from pathlib import Path
from typing import Dict, List, Optional

import easyocr

from src.domain.models import ContentType, DocumentContent


class ImageReader:
    _MIME_TYPES: Dict[str, str] = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }

    def __init__(self, supported_extensions: Optional[List[str]] = None):
        self._supported_extensions = supported_extensions or list(
            self._MIME_TYPES.keys()
        )
        self._reader = easyocr.Reader(["ru", "en"])

    def supports(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self._supported_extensions

    def read(self, file_path: Path) -> DocumentContent:
        text_content = self._extract_text_from_image(file_path)

        return DocumentContent(
            file_path=file_path,
            content_type=ContentType.TEXT,
            text_content=text_content,
            mime_type="text/plain",
        )

    def _extract_text_from_image(self, file_path: Path) -> str:
        """Extract text from image using EasyOCR."""
        try:
            # Read image and extract text
            results = self._reader.readtext(str(file_path), detail=0)

            # Combine all text results
            text = " ".join(results)

            return text.strip()
        except Exception as e:
            return f"Error extracting text from {file_path.name}: {str(e)}"

    def _get_mime_type(self, file_path: Path) -> str:
        return self._MIME_TYPES.get(file_path.suffix.lower(), "image/jpeg")

    def get_supported_extensions(self) -> List[str]:
        return self._supported_extensions
