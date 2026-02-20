from collections.abc import Callable
from typing import Any

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn


class FileProgress:
    def __init__(self, items: list[Any], description: str = "Processing"):
        self._items = items
        self._description = description
        self._progress = self._create_progress()

    def _create_progress(self) -> Progress:
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )

    def __enter__(self):
        self._progress.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._progress.stop()

    def track(self, callback: Callable[[Any], None]) -> None:
        task_id = self._progress.add_task(self._description, total=len(self._items))

        for item in self._items:
            self._update_item(task_id, item)
            callback(item)
            self._progress.advance(task_id)

    def _update_item(self, task_id: Any, item: Any) -> None:
        name = getattr(item, "name", str(item))
        self._progress.update(task_id, description=f"{self._description}: {name}")
