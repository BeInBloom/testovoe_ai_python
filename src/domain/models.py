from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from pathlib import Path
from typing import Optional


class ContentType(str, Enum):
    TEXT = "text"
    MULTIMODAL = "multimodal"


class DocumentContent(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    file_path: Path
    content_type: ContentType
    text_content: Optional[str] = None
    base64_data: Optional[str] = None
    mime_type: Optional[str] = None


class Document(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    path: Path
    size_bytes: int = Field(..., ge=0)
    content: DocumentContent
