from typing import Protocol

from rich.console import Console
from rich.panel import Panel


class OutputFormatter(Protocol):
    def format(self, summary: str) -> str: ...


class ConsoleFormatter:
    def format(self, summary: str) -> str:
        # Можно добавить markdown рендеринг в будущем
        return summary


class Formatter:
    def __init__(self, formatter: OutputFormatter):
        self._formatter = formatter
        self._console = Console()

    def output(self, summary: str) -> None:
        content = self._formatter.format(summary)
        panel = Panel(content, title="Summary", border_style="green")
        self._console.print(panel)
