import requests
from pydantic import BaseModel, Field, ValidationError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.core.logger import Logger
from src.domain.exceptions import LLMConnectionError, LLMResponseError
from src.llm.contracts import LLMProvider, Message


class LLMChoice(BaseModel):
    message: Message


class LLMResponse(BaseModel):
    choices: list[LLMChoice] = Field(..., min_length=1)


class OpenRouterLLMProvider(LLMProvider):
    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str,
        model: str,
        logger: Logger,
        timeout: int = 60,
    ):
        self._api_key = api_key
        self._model = model
        self._logger = logger
        self._timeout = timeout

    def generate_response(self, messages: list[Message]) -> str:
        payload = {
            "model": self._model,
            "messages": [msg.model_dump() for msg in messages],
        }
        return self._execute_interaction(payload)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(
            (requests.exceptions.RequestException, LLMConnectionError)
        ),
        reraise=True,
    )
    def _execute_interaction(self, payload: dict) -> str:
        headers = self._get_headers()

        self._logger.info(f"Sending request to {self.API_URL} (Model: {self._model})")

        try:
            response = requests.post(
                self.API_URL, headers=headers, json=payload, timeout=self._timeout
            )
            return self._process_response(response)

        except requests.exceptions.Timeout as e:
            self._logger.error("LLM API request timed out.")
            raise LLMConnectionError("Request to OpenRouter timed out.") from e

        except requests.exceptions.RequestException as e:
            self._logger.error(f"LLM request failed: {e}")
            raise LLMConnectionError(f"Connection error: {e}") from e

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "X-Title": "AI Document Summarizer",
        }

    def _process_response(self, response: requests.Response) -> str:
        if response.status_code != 200:
            self._handle_error(response)

        try:
            raw_data = response.json()
        except requests.exceptions.JSONDecodeError as e:
            self._logger.error(f"Received non-JSON response: {response.text[:200]}")
            raise LLMResponseError(
                "API returned invalid JSON (possibly a gateway error)."
            ) from e

        try:
            validated_data = LLMResponse.model_validate(raw_data)
            content = validated_data.choices[0].message.content
            if not isinstance(content, str):
                raise LLMResponseError(
                    "Expected text response from LLM, got multimodal object."
                )
            return content

        except ValidationError as e:
            self._logger.error(f"Failed to parse LLM response: {e}")
            raise LLMResponseError(f"Invalid response schema: {e}") from e

    def _handle_error(self, response: requests.Response) -> None:
        error_msg = response.text
        self._logger.error(f"API Error {response.status_code}: {error_msg}")

        if response.status_code == 404:
            raise LLMResponseError(f"Model not found: {self._model}")
        elif response.status_code == 401:
            raise LLMResponseError("Invalid OpenRouter API Key.")
        elif response.status_code == 429:
            raise LLMResponseError("Rate limit exceeded or insufficient funds.")

        response.raise_for_status()
