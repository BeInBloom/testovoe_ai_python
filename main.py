import sys
from pathlib import Path
from typing import Optional

import typer
from dependency_injector import providers

from config import AppConfig
from src.core.logger import Logger
from src.core.main_app import App
from src.dependencies import Container
from src.output.tables import display_error

cli_app = typer.Typer(name="ai-document-summarizer")


@cli_app.command()
def main(
    folder: Optional[Path] = typer.Argument(
        None, dir_okay=True, help="Папка с документами"
    ),
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p"),
    skill: Optional[str] = typer.Option(None, "--skill", "-s"),
    list_prompts: bool = typer.Option(False, "--list-prompts", "-l"),
    list_skills: bool = typer.Option(False, "--list-skills"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    try:
        # Инициализация
        logger = Logger(name="main", level="DEBUG" if verbose else "INFO")
        config = AppConfig()

        container = Container()
        container.config.from_pydantic(config)
        container.logger.override(providers.Object(logger))

        app = App(container)

        # Выполнение сценария
        if list_prompts:
            return app.list_prompts()
        if list_skills:
            return app.list_skills()

        app.run(folder, prompt, skill, verbose)

    except Exception as e:
        display_error(str(e), verbose)
        sys.exit(1)


if __name__ == "__main__":
    cli_app()
