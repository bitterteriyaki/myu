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

from discord import ClientUser, Intents, Message
from discord.ext.commands import Bot
from rich import print
from rich.box import ROUNDED
from rich.table import Table

log = getLogger(__name__)


class Myu(Bot):
    """The main bot class."""

    def __init__(self) -> None:
        super().__init__(command_prefix=get_prefix, intents=Intents.all())

    async def on_ready(self) -> None:
        user = cast(ClientUser, self.user)

        guilds = len(self.guilds)
        users = len(self.users)

        log.info(
            f"Logged in as 'user' (ID: {user.id}). "
            f"Connected to {guilds} guilds and {users} users."
        )

        columns = ("User", "ID", "Guilds", "Users")
        table = Table(*columns, box=ROUNDED)

        table.add_row(str(user), str(user.id), str(guilds), str(users))

        print(table)

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")


def get_prefix(bot: Myu, message: Message) -> tuple[str, ...]:
    return ("?", "myu ")
