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

from enum import IntEnum
from logging import getLogger
from os import environ
from typing import Any, cast

from discord import (
    Guild,
    Intents,
    Interaction,
    Message,
    Role,
    TextChannel,
)
from discord.ext.commands import Bot, Context
from discord.utils import cached_property
from jishaku.modules import find_extensions_in
from sqlalchemy.ext.asyncio import create_async_engine

from bot.utils.constants import GUILD_ID, STAFF_ROLE_IDS, TEST_CHANNEL_ID
from bot.utils.context import MyuContext
from bot.utils.database import DATABASE_URL

log = getLogger(__name__)


class Environment(IntEnum):
    """The environment the bot is running in."""

    DEVELOPMENT = 0
    PRODUCTION = 1
    UNKNOWN = 2


ENVIRONMENTS = {
    "development": Environment.DEVELOPMENT,
    "production": Environment.PRODUCTION,
}


class Myu(Bot):
    """The main bot class."""

    def __init__(self) -> None:
        super().__init__(command_prefix=get_prefix, intents=Intents.all())

        self.default_prefix = "!" if self.is_development() else "?"
        self.engine = create_async_engine(DATABASE_URL)

    @cached_property
    def environment(self) -> Environment:
        """The environment the bot is running in."""
        env = environ.get("BOT_ENV")

        if env is None:
            return Environment.UNKNOWN

        return ENVIRONMENTS.get(env, Environment.UNKNOWN)

    @cached_property
    def guild(self) -> Guild:
        return cast(Guild, self.get_guild(GUILD_ID))

    @cached_property
    def test_channel(self) -> TextChannel:
        return cast(TextChannel, self.guild.get_channel(TEST_CHANNEL_ID))

    @cached_property
    def staff_roles(self) -> tuple[Role, ...]:
        return tuple(
            cast(Role, self.guild.get_role(role_id))
            for role_id in STAFF_ROLE_IDS
        )

    def is_development(self) -> bool:
        """Return whether the bot is running in development environment.

        Returns
        -------
        :class:`bool`
            Whether the bot is running in development environment.
        """
        return self.environment == Environment.DEVELOPMENT

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
    return (bot.default_prefix, "myu ")
