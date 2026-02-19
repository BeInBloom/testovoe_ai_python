from pathlib import Path
from typing import Optional, TYPE_CHECKING
from src.core.logger import Logger

if TYPE_CHECKING:
    from src.dependencies import Container

class App:
    def __init__(self, container: "Container"):
        self._container = container
        self._logger = container.logger()
        self._prompt_manager = container.prompt_manager()
        self._document_service = container.document_service()
        self._summary_generator = container.summary_generator()
        self._formatter = container.formatter()

    def run(
        self, 
        folder: Optional[Path] = None, 
        prompt_name: Optional[str] = None, 
        skill_name: Optional[str] = None,
        verbose: bool = False
    ) -> None:
        """Основной сценарий анализа."""
        self._setup_logging(verbose)
        self._validate_folder(folder)
        
        prompt = self._prompt_manager.select(prompt_name, skill_name)
        documents = self._document_service.get_documents(folder)
        
        if documents:
            summary = self._summary_generator.generate(documents, prompt)
            self._formatter.output(summary)

    def list_prompts(self) -> None:
        """Сценарий отображения доступных промптов."""
        from src.output.tables import display_prompts_table
        registry = self._container.prompt_registry()
        registry.load()
        display_prompts_table(registry.list_prompts())

    def list_skills(self) -> None:
        """Сценарий отображения доступных скиллов."""
        from src.output.tables import display_skills_table
        registry = self._container.skill_registry()
        registry.load()
        display_skills_table(registry.list_skills())

    def _setup_logging(self, verbose: bool) -> None:
        if verbose:
            self._logger.set_level("DEBUG")
        self._logger.info("Initializing document analysis...")

    def _validate_folder(self, folder: Optional[Path]) -> None:
        if not folder:
            raise ValueError("Folder path is required. Please provide a path to the documents.")
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder}")
