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

from logging import getLogger
from typing import Any

from discord import Intents, Interaction, Message
from discord.ext.commands import Bot, Context
from jishaku.modules import find_extensions_in
from sqlalchemy.ext.asyncio import create_async_engine

from bot.utils.context import MyuContext
from bot.utils.database import DATABASE_URL

log = getLogger(__name__)


class Myu(Bot):
    """The main bot class."""

    def __init__(self) -> None:
        super().__init__(command_prefix=get_prefix, intents=Intents.all())

        self.engine = create_async_engine(DATABASE_URL)

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")

        for extesion in find_extensions_in("bot/extensions"):
            await self.load_extension(extesion)

    async def get_context(
        self,
        origin: Message | Interaction,
        /,
        *,
        cls: type[Context[Any]] = MyuContext,
    ) -> Any:
        return await super().get_context(origin, cls=cls)


def get_prefix(bot: Myu, message: Message) -> tuple[str, ...]:
    """Return the available prefixes for the bot in a given message.

    Parameters
    ----------
    bot: :class:`bot.core.Myu`
        The bot instance.
    message: :class:`discord.Message`
        The message object.

    Returns
    -------
    tuple[:class:`str`, ...]
        The available prefixes for the bot.
    """
    return ("?", "myu ")
