import traceback
from pathlib import Path

import typer
from dependency_injector import providers

from config import AppConfig
from src.core.logger import Logger
from src.core.main_app import App
from src.dependencies import Container
from src.output.tables import display_error

cli_app = typer.Typer(
    name="ai-document-summarizer",
    help="AI утилита для анализа и суммаризации документов",
    no_args_is_help=True,
)


def bootstrap_app(verbose: bool) -> App:
    logger = Logger(name="main", level="DEBUG" if verbose else "INFO")
    config = AppConfig()

    container = Container()
    container.config.from_pydantic(config)
    container.logger.override(providers.Object(logger))

    return App(container)


def handle_exception(e: Exception, verbose: bool):
    if verbose:
        traceback.print_exc()
    display_error(str(e), verbose)
    raise typer.Exit(code=1)


@cli_app.command(name="run")
def run_analysis(
    folder: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        help="Путь к папке с документами",
    ),
    prompt: str | None = typer.Option(
        None, "--prompt", "-p", help="Имя промпта для генерации"
    ),
    skill: str | None = typer.Option(None, "--skill", "-s", help="Навык для обработки"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Детальное логирование"),
):
    try:
        app = bootstrap_app(verbose)
        app.run(folder, prompt, skill, verbose)
    except Exception as e:
        handle_exception(e, verbose)


@cli_app.command(name="list-prompts")
def list_prompts(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Детальное логирование"),
):
    try:
        app = bootstrap_app(verbose)
        app.list_prompts()
    except Exception as e:
        handle_exception(e, verbose)


@cli_app.command(name="list-skills")
def list_skills(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Детальное логирование"),
):
    try:
        app = bootstrap_app(verbose)
        app.list_skills()
    except Exception as e:
        handle_exception(e, verbose)


if __name__ == "__main__":
    # suppress_third_party_noise()
    cli_app()
