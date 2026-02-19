from pathlib import Path

import pytest

from src.domain.models import ContentType
from src.readers.image_reader import ImageReader
from src.readers.pdf_reader import PdfReader
from src.readers.txt_reader import TxtReader


def test_txt_reader_success(tmp_path):
    p = tmp_path / "hello.txt"
    p.write_text("Hello World", encoding="utf-8")

    reader = TxtReader()
    assert reader.supports(p)

    content = reader.read(p)
    assert content.content_type == ContentType.TEXT
    assert content.text_content == "Hello World"
    assert content.file_path == p


def test_txt_reader_unsupported_extension():
    reader = TxtReader()
    assert not reader.supports(Path("image.png"))


def test_image_reader_success(tmp_path):
    p = tmp_path / "test.png"
    # Basic PNG signature
    p.write_bytes(b"\x89PNG\r\n\x1a\n")

    reader = ImageReader()
    assert reader.supports(p)

    content = reader.read(p)
    assert content.content_type == ContentType.MULTIMODAL
    assert content.mime_type == "image/png"
    assert len(content.base64_data) > 0


def test_pdf_reader_success(tmp_path):
    p = tmp_path / "test.pdf"
    p.write_bytes(b"%PDF-1.4")

    reader = PdfReader()
    assert reader.supports(p)

    content = reader.read(p)
    assert content.content_type == ContentType.MULTIMODAL
    assert content.mime_type == "application/pdf"
    assert len(content.base64_data) > 0


def test_txt_reader_encoding_error(tmp_path):
    # Creating a file with invalid utf-8 sequence
    p = tmp_path / "bad.txt"
    p.write_bytes(b"\xff\xfe\xfd")

    reader = TxtReader()
    with pytest.raises(UnicodeDecodeError):
        reader.read(p)
