from pathlib import Path
from typing import List

from src.core.document_collector import DocumentCollector
from src.core.folder_scanner import FolderScanner
from src.core.logger import Logger
from src.domain.models import Document


class DocumentService:
    def __init__(
        self, scanner: FolderScanner, collector: DocumentCollector, logger: Logger
    ):
        self._scanner = scanner
        self._collector = collector
        self._logger = logger

    def get_documents(self, folder_path: Path) -> List[Document]:
        """Оркестрирует поиск и загрузку документов."""
        self._logger.info(f"Scanning folder: {folder_path}")

        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        # Собираем пути из генератора
        file_paths = list(self._scanner.scan(folder_path))

        if not file_paths:
            self._logger.warning(f"No files found in {folder_path}")
            return []

        documents = self._collector.collect(file_paths)
        self._logger.info(f"Loaded {len(documents)} valid documents")

        return documents
