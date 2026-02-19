from typing import Any, Dict

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def _display_registry_table(title: str, items: Dict[str, Any]) -> None:
    """Общий рендерер для таблиц из реестра."""
    console = Console()
    table = Table(title=title, box=box.SIMPLE)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for name, item in items.items():
        description = getattr(item, "description", "")
        table.add_row(name, description)

    console.print(table)


def display_prompts_table(prompts: Dict[str, Any]) -> None:
    _display_registry_table("Available Prompts", prompts)


def display_skills_table(skills: Dict[str, Any]) -> None:
    _display_registry_table("Available Skills", skills)


def display_error(message: str, verbose: bool = False) -> None:
    """Красивый вывод ошибки."""
    console = Console()
    panel = Panel(message, title="Error", border_style="red")
    console.print(panel)

    if verbose:
        console.print_exception()
