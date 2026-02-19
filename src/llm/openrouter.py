import logging
import requests
from typing import Any, List, Dict, Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

from src.core.logger import Logger
from src.domain.exceptions import LLMConnectionError, LLMResponseError
from src.domain.models import ContentType, Document
from src.llm.contracts import LLMProvider


class OpenRouterLLMProvider(LLMProvider):
    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str,
        model: str,
        logger: Logger,
        timeout: int = 10,
        max_retries: int = 3,
    ):
        self._api_key = api_key
        self._model = model
        self._logger = logger
        self._timeout = timeout
        self._max_retries = max_retries

    def generate_summary(self, documents: List[Document], prompt: str) -> str:
        """Оркестрирует подготовку данных и выполнение запроса."""
        content = self._build_content(documents, prompt)
        messages = [{"role": "user", "content": content}]
        return self._execute_interaction(messages)

    def _build_content(
        self, documents: List[Document], prompt: str
    ) -> List[Dict[str, Any]]:
        """Собирает контент сообщения из промпта и документов."""
        content: List[Dict[str, Any]] = [{"type": "text", "text": prompt}]
        for doc in documents:
            item = self._format_document_item(doc)
            if item:
                content.append(item)
        return content

    def _format_document_item(self, doc: Document) -> Optional[Dict[str, Any]]:
        """Форматирует один документ в структуру API."""
        if doc.content.content_type in [ContentType.TEXT, ContentType.MULTIMODAL]:
            return {
                "type": "text",
                "text": f"\n\n--- {doc.path.name} ---\n{doc.content.text_content}",
            }
        return None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(
            (requests.exceptions.RequestException, LLMConnectionError)
        ),
        reraise=True,
    )
    def _execute_interaction(self, messages: List[Dict[str, Any]]) -> str:
        """Выполняет сетевой запрос и обрабатывает результат."""
        headers = self._get_headers()
        payload = {"model": self._model, "messages": messages}

        self._logger.info(f"Sending request to {self.API_URL}")
        self._logger.info(f"Payload: {payload}")

        try:
            response = requests.post(
                self.API_URL, headers=headers, json=payload, timeout=self._timeout
            )
            self._logger.info(f"Response status: {response.status_code}")
            return self._process_response(response)
        except requests.exceptions.RequestException as e:
            self._logger.error(f"LLM request failed: {str(e)}")
            raise LLMConnectionError(f"Connection error: {str(e)}")

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ai-document-summarizer",
            "X-Title": "AI Document Summarizer",
        }

    def _process_response(self, response: requests.Response) -> str:
        """Валидирует и парсит ответ API."""
        if response.status_code != 200:
            self._handle_error(response)

        data = response.json()
        if not data.get("choices"):
            raise LLMResponseError("Invalid response format: no choices found")

        return data["choices"][0]["message"]["content"]

    def _handle_error(self, response: requests.Response) -> None:
        """Обработка ошибок API."""
        error_msg = response.text
        self._logger.error(f"API Error {response.status_code}: {error_msg}")

        if response.status_code == 404:
            raise LLMResponseError(f"Model not found: {self._model}")

        response.raise_for_status()
