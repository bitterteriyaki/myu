from discord.ext.commands import Bot
from discord import Intents


class Myu(Bot):
    """The main bot class."""

    def __init__(self) -> None:
        super().__init__(command_prefix=get_prefix, intents=Intents.all())


def get_prefix(bot, message):
    return ("?", "myu ")
