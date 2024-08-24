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

from typing import cast

from discord import Member
from discord.ext.commands import Author, Cog, hybrid_command
from sqlalchemy import select

from bot.core import Myu
from bot.utils.constants import COIN_EMOJI
from bot.utils.context import MyuContext
from bot.utils.database import User


class Economy(Cog):
    """Commands related to the economy system."""

    def __init__(self, bot: Myu) -> None:
        self.bot = bot

    async def get_balance(self, user_id: int, /) -> int:
        async with self.bot.engine.begin() as conn:
            stmt = select(User.balance).where(User.id == user_id)
            result = (await conn.execute(stmt)).fetchone()

        return cast(int, result.balance) if result is not None else 0

    @hybrid_command(aliases=["bal"])  # type: ignore
    async def balance(
        self, ctx: MyuContext, *, member: Member = Author
    ) -> None:
        balance = await self.get_balance(member.id)
        await ctx.reply(f"{member.mention} possui {balance} {COIN_EMOJI}.")


async def setup(bot: Myu) -> None:
    await bot.add_cog(Economy(bot))
