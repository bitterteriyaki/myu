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

from collections.abc import Callable
from datetime import timedelta
from logging import getLogger
from typing import cast

from discord import ClientUser, Message
from discord.ext.commands import (
    Cog,
    CommandError,
    CommandOnCooldown,
)
from humanize import precisedelta
from rich import print
from rich.box import ROUNDED
from rich.table import Table

from bot.core import Myu
from bot.utils.context import MyuContext

log = getLogger(__name__)


class Events(Cog):
    """Event listeners for the bot."""

    def __init__(self, bot: Myu) -> None:
        self.bot = bot
        self.error_callbacks = cast(
            dict[type[CommandError], Callable[[CommandError], str]],
            {CommandOnCooldown: self.on_command_on_cooldown},
        )

    def on_command_on_cooldown(self, error: CommandOnCooldown) -> str:
        delta = timedelta(seconds=error.retry_after)
        retry_after = precisedelta(delta, format="%0.0f")

        return f"Você poderá usar esse comando novamente em **{retry_after}**."

    @Cog.listener()
    async def on_ready(self) -> None:
        bot = self.bot
        user = cast(ClientUser, bot.user)

        guilds = len(bot.guilds)
        users = len(bot.users)

        message = (
            "Logged in as '%s' (ID: %d). "
            "Connected to %d guilds and %d users."
        )

        log.info(message, user, user.id, guilds, users)

        columns = ("User", "ID", "Guilds", "Users")
        table = Table(*columns, box=ROUNDED)
        table.add_row(str(user), str(user.id), str(guilds), str(users))

        print(table)

    @Cog.listener()
    async def on_command_error(
        self, ctx: MyuContext, error: CommandError
    ) -> None:
        callback = self.error_callbacks.get(type(error))

        if callback is None:
            raise error

        await ctx.reply(callback(error))

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return

        self.bot.dispatch("regular_message", message)


async def setup(bot: Myu) -> None:
    await bot.add_cog(Events(bot))
