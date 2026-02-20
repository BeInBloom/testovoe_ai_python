from pathlib import Path

from src.readers.contracts import DocumentReader


class ReaderFactory:
    def __init__(self, readers: list[DocumentReader]):
        self._readers = readers

    def get_reader(self, file_path: Path) -> DocumentReader | None:
        for reader in self._readers:
            if reader.supports(file_path):
                return reader
        return None

    def get_all_supported_extensions(self) -> list[str]:
        extensions = []
        for reader in self._readers:
            extensions.extend(reader.get_supported_extensions())
        return list(set(extensions))
