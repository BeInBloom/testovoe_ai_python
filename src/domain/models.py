from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class ContentType(str, Enum):
    TEXT = "text"
    MULTIMODAL = "multimodal"


class DocumentContent(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    file_path: Path
    content_type: ContentType
    text_content: str | None = None
    base64_data: str | None = None
    mime_type: str | None = None


class Document(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    path: Path
    size_bytes: int = Field(..., ge=0)
    content: DocumentContent
