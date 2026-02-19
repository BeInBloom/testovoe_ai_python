from pathlib import Path
from typing import List, Optional

from src.readers.contracts import DocumentReader


class ReaderFactory:
    def __init__(self, readers: List[DocumentReader]):
        self._readers = readers

    def get_reader(self, file_path: Path) -> Optional[DocumentReader]:
        for reader in self._readers:
            if reader.supports(file_path):
                return reader
        return None

    def get_all_supported_extensions(self) -> List[str]:
        extensions = []
        for reader in self._readers:
            extensions.extend(reader.get_supported_extensions())
        return list(set(extensions))
