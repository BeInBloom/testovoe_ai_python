from pathlib import Path

from src.core.logger import Logger
from src.domain.exceptions import DocumentReadError
from src.domain.models import Document
from src.readers.factory import ReaderFactory


class DocumentCollector:
    def __init__(
        self,
        reader_factory: ReaderFactory,
        logger: Logger,
        max_file_size_bytes: int = 10 * 1024 * 1024,  # 10MB default
    ):
        self._reader_factory = reader_factory
        self._logger = logger
        self._max_file_size_bytes = max_file_size_bytes

    def collect(self, file_paths: list[Path]) -> list[Document]:
        documents = []

        for file_path in file_paths:
            if self._should_skip(file_path):
                continue

            try:
                document = self._read_document(file_path)
                if document:
                    documents.append(document)
                    self._logger.info(f"Collected: {file_path}")
            except Exception as e:
                self._logger.exception(f"Failed to read {file_path}: {e}")
                raise DocumentReadError(f"Failed to read {file_path}: {e}")

        return documents

    def _should_skip(self, file_path: Path) -> bool:
        if file_path.name.startswith("."):
            return True

        if not file_path.is_file():
            return True

        try:
            file_size = file_path.stat().st_size
            if file_size > self._max_file_size_bytes:
                self._logger.warning(
                    f"File too large ({file_size} bytes), skipping: {file_path}"
                )
                return True
        except OSError:
            return True

        reader = self._reader_factory.get_reader(file_path)
        if reader is None:
            self._logger.debug(f"No reader for {file_path}, skipping.")
            return True

        return False

    def _read_document(self, file_path: Path) -> Document | None:
        reader = self._reader_factory.get_reader(file_path)
        if not reader:
            return None

        content = reader.read(file_path)
        size_bytes = file_path.stat().st_size

        return Document(path=file_path, size_bytes=size_bytes, content=content)
