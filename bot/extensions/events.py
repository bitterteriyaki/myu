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
from typing import cast

from discord import ClientUser, Message
from discord.ext.commands import Cog
from rich import print
from rich.box import ROUNDED
from rich.table import Table

from bot.core import Myu

log = getLogger(__name__)


class Events(Cog):
    """Event listeners for the bot."""

    def __init__(self, bot: Myu) -> None:
        self.bot = bot

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
    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return

        self.bot.dispatch("regular_message", message)


async def setup(bot: Myu) -> None:
    await bot.add_cog(Events(bot))
