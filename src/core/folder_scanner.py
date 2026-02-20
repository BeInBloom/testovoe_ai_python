from collections.abc import Generator
from pathlib import Path

from src.core.logger import Logger


class FolderScanner:
    def __init__(
        self,
        logger: Logger,
        recursive: bool = True,
    ):
        self._logger = logger
        self._recursive = recursive

    def scan(self, folder_path: Path) -> Generator[Path]:
        try:
            for item in folder_path.iterdir():
                if item.is_file():
                    yield item
                elif item.is_dir() and self._recursive:
                    if not item.name.startswith("."):
                        yield from self.scan(item)

        except PermissionError:
            self._logger.warning(f"Permission denied: {folder_path}")
