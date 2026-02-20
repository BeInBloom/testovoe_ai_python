from dependency_injector import containers, providers

from src.core.document_collector import DocumentCollector
from src.core.document_service import DocumentService
from src.core.folder_scanner import FolderScanner
from src.core.logger import Logger
from src.core.prompt_manager import PromptManager
from src.core.summary_generator import SummaryGenerator
from src.llm.openrouter import OpenRouterLLMProvider
from src.output.formatter import ConsoleFormatter, Formatter
from src.prompts.registry import PromptRegistry
from src.readers.factory import ReaderFactory
from src.readers.pdf_reader import PdfReader
from src.readers.txt_reader import TxtReader
from src.skills.registry import SkillRegistry


def _mb_to_bytes(mb: int) -> int:
    return mb * 1024 * 1024


def _create_audio_video_reader():
    from src.readers.audio_vide_reader import AudioVideoReader

    return AudioVideoReader()


def _create_image_reader():
    from src.readers.image_reader import ImageReader

    return ImageReader()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(
        Logger,
        name="main",
        level="INFO",
    )

    prompt_registry = providers.Singleton(
        PromptRegistry,
        prompts_path=config.prompts_path,
    )

    skill_registry = providers.Singleton(
        SkillRegistry,
        skills_path=config.skills_path,
        logger=logger,
    )

    prompt_manager = providers.Singleton(
        PromptManager,
        prompt_registry=prompt_registry,
        skill_registry=skill_registry,
        logger=logger,
    )

    txt_reader = providers.Singleton(TxtReader)
    pdf_reader = providers.Singleton(PdfReader)
    image_reader = providers.Singleton(_create_image_reader)
    video_audio_reader = providers.Singleton(_create_audio_video_reader)

    reader_factory = providers.Singleton(
        ReaderFactory,
        readers=providers.List(
            txt_reader.provided,
            pdf_reader.provided,
            image_reader.provided,
            video_audio_reader.provided,
        ),
    )

    llm_client = providers.Singleton(
        OpenRouterLLMProvider,
        api_key=config.openrouter_api_key,
        model=config.openrouter_model,
        logger=logger,
        timeout=config.request_timeout,
    )

    max_file_size_bytes = providers.Callable(
        _mb_to_bytes,
        config.max_file_size_mb,
    )

    folder_scanner = providers.Singleton(
        FolderScanner,
        logger=logger,
        recursive=config.recursive_scan,
    )

    document_collector = providers.Singleton(
        DocumentCollector,
        reader_factory=reader_factory,
        logger=logger,
        max_file_size_bytes=max_file_size_bytes,
    )

    document_service = providers.Singleton(
        DocumentService,
        scanner=folder_scanner,
        collector=document_collector,
        logger=logger,
    )

    summary_generator = providers.Singleton(
        SummaryGenerator,
        llm_provider=llm_client,
        logger=logger,
    )

    console_formatter = providers.Singleton(ConsoleFormatter)

    formatter = providers.Singleton(
        Formatter,
        formatter=console_formatter,
    )
