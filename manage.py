from os import environ
from contextlib import contextmanager
from collections.abc import Generator
from logging import getLogger, INFO, WARN, Formatter
from logging.handlers import RotatingFileHandler

from click import group

from bot.core import Myu


@contextmanager
def setup_logging() -> Generator[None, None, None]:
    log = getLogger()

    try:
        max_bytes = 32 * 1024 * 1024

        getLogger("discord").setLevel(INFO)
        getLogger("discord.http").setLevel(WARN)

        log.setLevel(INFO)

        handler = RotatingFileHandler(
            "logs/myu.log",
            encoding="utf-8",
            maxBytes=max_bytes,
            backupCount=5,
        )

        datetime_format = "%Y-%m-%d %H:%M:%S"
        log_format = "[{asctime}] [{levelname}] {name}: {message}"

        formatter = Formatter(log_format, datetime_format, style="{")

        handler.setFormatter(formatter)
        log.addHandler(handler)

        yield
    finally:
        for handler in log.handlers[:]:
            handler.close()
            log.removeHandler(handler)


@group()
def main() -> None:
    """Initial entrypoint for the bot."""


@main.command()
def runbot() -> None:
    """Run the bot."""
    with setup_logging():
        bot = Myu()
        token = environ["DISCORD_TOKEN"]

        bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()
