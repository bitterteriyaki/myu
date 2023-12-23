"""
Copyright (C) 2024-present kyomi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from collections.abc import Generator
from contextlib import contextmanager
from logging import INFO, WARNING, Formatter, getLogger
from logging.handlers import RotatingFileHandler
from os import environ
from typing import cast

from click import group

from bot.core import Myu


@contextmanager
def setup_logging() -> Generator[None, None, None]:
    log = getLogger()

    try:
        max_bytes = 32 * 1024 * 1024

        getLogger("discord").setLevel(INFO)
        getLogger("discord.http").setLevel(WARNING)

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
        for handler in cast(list[RotatingFileHandler], log.handlers):
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
