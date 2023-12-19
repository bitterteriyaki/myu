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
from random import randint
from typing import cast

from discord import Message
from discord.ext.commands import BucketType, Cog, CooldownMapping
from sqlalchemy import insert, select, update

from bot.core import Myu
from bot.utils.database import User
from bot.utils.embed import generate_embed

log = getLogger(__name__)


class Levels(Cog):
    """Ranking system for users."""

    __slots__ = ("bot",)

    def __init__(self, bot: Myu) -> None:
        self.bot = bot
        # Users can only gain experience once every minute. This is
        # because we don't want users to spam messages to gain
        # experience.
        self.cooldown = CooldownMapping.from_cooldown(1, 60, BucketType.user)

    def get_level_exp(self, level: int) -> int:
        """Get the experience require to reach the given level. The
        formula used to calculate the experience is:

        .. code-block:: python

            5 * (level**2) + (50 * level) + 100

        Parameters
        ----------
        level: :class:`int`
            The level to get the experience required to reach it.

        Returns
        -------
        :class:`int`
            The experience required to reach the given level.
        """
        return 5 * (level**2) + (50 * level) + 100

    def get_level_from_exp(self, exp: int) -> int:
        """Get the level from the given experience.

        Parameters
        ----------
        exp: :class:`int`
            The experience to get the level from.

        Returns
        -------
        :class:`int`
            The level from the given experience.
        """
        level = 0

        while exp >= (needed_exp := self.get_level_exp(level)):
            exp -= needed_exp
            level += 1

        return level

    async def insert_user(self, user_id: int) -> None:
        """Insert an user into database with the given ID and default
        experience of 0. This should only be used when the user sends
        a message and doesn't exist in the database.

        Parameters
        ----------
        user_id: :class:`int`
            The ID of the user to insert into the database.
        """
        async with self.bot.engine.begin() as conn:
            stmt = insert(User).values(id=user_id)
            await conn.execute(stmt)

    async def get_experience(
        self, user_id: int, /, *, insert: bool = False
    ) -> int:
        """Get the experience of an user with the given ID. If the user
        doesn't exist in the database, then zero is returned. If the
        ``insert`` parameter is set to ``True``, then the user will be
        insert into the database if it doesn't exist.

        Parameters
        ----------
        user_id: :class:`int`
            The ID of the user to get the experience from.
        insert: :class:`bool`
            Whether to insert the user into the database if it doesn't
            exist. Defaults to ``False``.

        Returns
        -------
        :class:`int`
            The experience of the user with the given ID.
        """
        async with self.bot.engine.begin() as conn:
            stmt = select(User).where(User.id == user_id)
            result = (await conn.execute(stmt)).fetchone()

        if result is None and insert is True:
            await self.insert_user(user_id)

        return cast(int, result.exp) if result is not None else 0

    async def add_experience(self, user_id: int, to_add: int) -> int:
        """Add experience to an user with the given ID. If the user
        doesn't exist in the database, then zero is returned. If the
        user exists in the database, then zero is returned.

        Parameters
        ----------
        user_id: :class:`int`
            The ID of the user to add the experience to.
        to_add: :class:`int`
            The amount of experience to add to the user.

        Returns
        -------
        :class:`int`
            The new experience of the user with the given ID.
        """
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

        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit() if bucket else None

        if retry_after is not None:
            return

        to_add = randint(15, 25)

        new_exp = await self.add_experience(author.id, to_add)
        new_level = self.get_level_from_exp(new_exp)

        log.info(
            "User '%s' (ID: %s) received %d experience (%s -> %s).",
            author,
            author.id,
            to_add,
            current_exp,
            new_exp,
        )

        if new_level > current_level:
            content = f"{author.mention} has leveled up to level {new_level}!"
            embed = generate_embed(content, member=author)
            await message.reply(embed=embed, mention_author=False)


async def setup(bot: Myu) -> None:
    await bot.add_cog(Levels(bot))
