import pytest
import requests
import requests_mock
from pathlib import Path
from src.llm.openrouter import OpenRouterLLMProvider
from src.domain.models import Document, DocumentContent, ContentType
from src.domain.exceptions import LLMResponseError, LLMConnectionError
from src.core.logger import Logger

@pytest.fixture
def logger():
    return Logger(name="test", level="DEBUG")

@pytest.fixture
def provider(logger):
    return OpenRouterLLMProvider(
        api_key="test_key",
        model="test_model",
        logger=logger,
        timeout=1
    )

def test_generate_summary_success(provider):
    with requests_mock.Mocker() as m:
        m.post(provider.API_URL, json={
            "choices": [{"message": {"content": "Test summary"}}]
        })
        
        doc = Document(
            path=Path("test.txt"),
            size_bytes=10,
            content=DocumentContent(
                file_path=Path("test.txt"),
                content_type=ContentType.TEXT,
                text_content="Hello world"
            )
        )
        
        result = provider.generate_summary([doc], "Summarize this")
        assert result == "Test summary"
        assert m.called
        
        # Проверка payload
        last_request = m.request_history[0].json()
        assert last_request["model"] == "test_model"
        assert "Summarize this" in last_request["messages"][0]["content"][0]["text"]

def test_handle_404_model_not_found(provider):
    with requests_mock.Mocker() as m:
        m.post(provider.API_URL, status_code=404, text="Model not found")
        
        doc = Document(
            path=Path("test.txt"),
            size_bytes=10,
            content=DocumentContent(
                file_path=Path("test.txt"),
                content_type=ContentType.TEXT,
                text_content="Hello"
            )
        )
        
        with pytest.raises(LLMResponseError) as excinfo:
            provider.generate_summary([doc], "prompt")
        assert "Model not found" in str(excinfo.value)

def test_retry_on_connection_error(provider, mocker):
    # Уменьшаем время ожидания для быстрого теста
    mocker.patch("tenacity.nap.time.sleep", return_value=None)
    
    with requests_mock.Mocker() as m:
        # Используем requests.exceptions.ConnectionError, который входит в RequestException
        m.post(provider.API_URL, [
            {"exc": requests.exceptions.ConnectionError()},
            {"json": {"choices": [{"message": {"content": "Finally success"}}]}}
        ])
        
        doc = Document(
            path=Path("test.txt"),
            size_bytes=10,
            content=DocumentContent(
                file_path=Path("test.txt"),
                content_type=ContentType.TEXT,
                text_content="Hello"
            )
        )
        
        result = provider.generate_summary([doc], "prompt")
        assert result == "Finally success"
        assert m.call_count == 2

def test_format_multimodal_image(provider):
    doc = Document(
        path=Path("test.png"),
        size_bytes=100,
        content=DocumentContent(
            file_path=Path("test.png"),
            content_type=ContentType.MULTIMODAL,
            base64_data="base64string",
            mime_type="image/png"
        )
    )
    
    item = provider._format_document_item(doc)
    assert item["type"] == "image_url"
    assert "data:image/png;base64,base64string" in item["image_url"]["url"]

def test_invalid_response_format(provider):
    with requests_mock.Mocker() as m:
        m.post(provider.API_URL, json={"wrong": "format"})
        
        doc = Document(
            path=Path("test.txt"),
            size_bytes=10,
            content=DocumentContent(
                file_path=Path("test.txt"),
                content_type=ContentType.TEXT,
                text_content="Hello"
            )
        )
        
        with pytest.raises(LLMResponseError) as excinfo:
            provider.generate_summary([doc], "prompt")
        assert "no choices found" in str(excinfo.value)
