from src.core.logger import Logger
from src.domain.models import ContentType, Document
from src.llm.contracts import LLMProvider, Message  # Message теперь живет в контрактах


class SummaryGenerator:
    def __init__(self, llm_provider: LLMProvider, logger: Logger):
        self._llm = llm_provider
        self._logger = logger

    def generate(
        self,
        documents: list[Document],
        user_prompt: str,
        system_prompt: str | None = "You are an expert editor and summarizer.",
    ) -> str:
        self._logger.info(f"Starting summary generation for {len(documents)} documents.")

        context_text = self._build_context_from_docs(documents)
        if not context_text.strip():
            self._logger.warning("No valid text found in documents to summarize.")
            return "Не удалось сгенерировать саммари: в документах нет поддерживаемого текста."

        messages = self._build_messages(context_text, user_prompt, system_prompt)

        self._logger.info("Sending prepared messages to LLM provider...")
        return self._llm.generate_response(messages)

    def _build_context_from_docs(self, documents: list[Document]) -> str:
        parts = []
        for doc in documents:
            if doc.content.content_type in [ContentType.TEXT, ContentType.MULTIMODAL]:
                formatted_doc = f"--- {doc.path.name} ---\n{doc.content.text_content}"
                parts.append(formatted_doc)
            else:
                self._logger.debug(
                    f"Skipping document {doc.path.name}: "
                    f"unsupported type {doc.content.content_type}"
                )
        return "\n\n".join(parts)

    def _build_messages(
        self, context: str, user_prompt: str, system_prompt: str | None
    ) -> list[Message]:
        messages: list[Message] = []

        if system_prompt:
            messages.append(Message(role="system", content=system_prompt))

        final_user_content = f"{user_prompt}\n\nКонтекст документов:\n{context}"
        messages.append(Message(role="user", content=final_user_content))
        return messages
