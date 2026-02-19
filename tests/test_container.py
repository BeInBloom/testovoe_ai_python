from src.core.document_service import DocumentService
from src.core.logger import Logger
from src.dependencies import Container


def test_container_wiring():
    container = Container()
    container.config.from_dict(
        {
            "prompts_path": "prompts",
            "skills_path": "skills",
            "openrouter_api_key": "key",
            "openrouter_model": "model",
            "request_timeout": 10,
            "max_retries": 3,
            "max_file_size_mb": 10,
            "recursive_scan": True,
        }
    )

    # Проверка синглтонов
    logger1 = container.logger()
    logger2 = container.logger()
    assert logger1 is logger2
    assert isinstance(logger1, Logger)

    # Проверка цепочки зависимостей
    doc_service = container.document_service()
    assert isinstance(doc_service, DocumentService)


def test_container_configuration_override():
    container = Container()
    container.config.from_dict({"max_file_size_mb": 5})

    # _mb_to_bytes(5) -> 5242880
    assert container.max_file_size_bytes() == 5242880
