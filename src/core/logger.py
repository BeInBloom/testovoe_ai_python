import sys
from loguru import logger


class Logger:
    _configured = False

    def __init__(self, name: str, level: str = "INFO"):
        self._name = name
        self._level = level
        self._logger = logger.bind(name=name)

        if not Logger._configured:
            self._configure(level)
            Logger._configured = True

    def _configure(self, level: str) -> None:
        logger.remove()
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[name]}</cyan> - <level>{message}</level>",
            level=level,
            colorize=True,
        )

    def debug(self, msg: str) -> None:
        self._logger.debug(msg)

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)

    def exception(self, msg: str) -> None:
        self._logger.exception(msg)

    def set_level(self, level: str) -> None:
        self._level = level
        self._configure(level)
