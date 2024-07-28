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

from random import randint
from typing import cast

from discord import Message
from discord.ext.commands import Cog
from sqlalchemy import insert, select, update

from bot.core import Myu
from bot.utils.database import User
from bot.utils.embed import generate_embed


class Levels(Cog):
    """Ranking system for users."""

    __slots__ = ("bot",)

    def __init__(self, bot: Myu) -> None:
        self.bot = bot

    def get_level_exp(self, level: int) -> int:
        """ """
        return 5 * (level**2) + (50 * level) + 100

    def get_level_from_exp(self, exp: int) -> int:
        """ """
        level = 0

        while exp >= (needed_exp := self.get_level_exp(level)):
            exp -= needed_exp
            level += 1

        return level

    async def insert_user(self, user_id: int) -> None:
        """ """
        async with self.bot.engine.begin() as conn:
            stmt = insert(User).values(id=user_id)
            await conn.execute(stmt)

    async def get_experience(
        self, user_id: int, /, *, insert: bool = False
    ) -> int:
        """ """
        async with self.bot.engine.begin() as conn:
            stmt = select(User).where(User.id == user_id)
            result = (await conn.execute(stmt)).fetchone()

        if result is None and insert is True:
            await self.insert_user(user_id)

        return cast(int, result.exp) if result is not None else 0

    async def add_experience(self, user_id: int, to_add: int) -> int:
        """ """
        async with self.bot.engine.begin() as conn:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(exp=User.exp + to_add)
                .returning(User.exp)
            )
            result = (await conn.execute(stmt)).fetchone()

        return cast(int, result.exp) if result is not None else 0

    @Cog.listener()
    async def on_regular_message(self, message: Message) -> None:
        author = message.author

        current_exp = await self.get_experience(author.id, insert=True)
        current_level = self.get_level_from_exp(current_exp)

        new_exp = await self.add_experience(author.id, randint(15, 25))
        new_level = self.get_level_from_exp(new_exp)

        if new_level > current_level:
            content = f"{author.mention} has leveled up to level {new_level}!"
            embed = generate_embed(content, member=author)
            await message.reply(embed=embed, mention_author=False)


async def setup(bot: Myu) -> None:
    await bot.add_cog(Levels(bot))
