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

from asyncio import TimeoutError
from random import randint
from typing import cast

from discord import Reaction, User
from discord.ext.commands import Cog
from discord.ext.tasks import loop

from bot.core import Myu
from bot.extensions.economy import Economy
from bot.utils.embed import generate_embed


class Lootboxes(Cog):
    """Commands related to lootboxes."""

    def __init__(self, bot: Myu) -> None:
        self.bot = bot
        self.emoji = "\U0001f381"

    @Cog.listener()
    async def on_ready(self) -> None:
        self.channel = (
            self.bot.test_channel
            if self.bot.is_development()
            else self.bot.chat_channel
        )
        self.economy = cast(Economy, self.bot.get_cog("Economy"))

        self.drop_lootbox.start()

    @loop(minutes=15)
    async def drop_lootbox(self) -> None:
        embed = generate_embed()
        embed.title = f"Uma lootbox selvagem apareceu! {self.emoji}"
        embed.description = (
            "Reaja esta mensagem com o emoji indicado "
            "para pegar a sua lootbox!"
        )

        message = await self.channel.send(embed=embed)
        await message.add_reaction(self.emoji)

        def check(reaction: Reaction, user: User) -> bool:
            return (
                reaction.message.id == message.id
                and str(reaction.emoji) == self.emoji
            )

        try:
            _, user = await self.bot.wait_for(
                "reaction_add", check=check, timeout=60
            )
        except TimeoutError:
            await message.delete()

            embed = generate_embed()
            embed.title = (
                f"Ninguém pegou a lootbox, logo ela desapareceu! {self.emoji}"
            )

            await self.channel.send(embed=embed, delete_after=12)
            return

        await message.delete()

        amount = randint(10, 75)
        await self.economy.add_coins(user.id, amount)

        embed = generate_embed(member=user)
        embed.title = f"Lootbox obtida! {self.emoji}"
        embed.description = (
            f"{user.mention} pegou a sua lootbox e recebeu {amount} coins."
        )

        await self.channel.send(embed=embed, delete_after=12)


async def setup(bot: Myu) -> None:
    await bot.add_cog(Lootboxes(bot))
