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

from discord import HTTPException, Member
from discord.ext.commands import Cog, has_permissions, hybrid_command

from bot.core import Myu
from bot.utils.context import MyuContext


def is_member_staff(ctx: MyuContext, member: Member) -> bool:
    return any(role in ctx.bot.staff_roles for role in member.roles)


class Moderation(Cog):
    """Commands for moderating the server."""

    def __init__(self, bot: Myu) -> None:
        self.bot = bot

    @hybrid_command()  # type: ignore
    @has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: MyuContext,
        member: Member,
        *,
        reason: str | None = None,
    ) -> None:
        """Bans a member from the server."""
        if is_member_staff(ctx, member):
            await ctx.reply("Você não pode banir um membro da equipe.")
            return

        try:
            await ctx.guild.ban(member, reason=reason)
        except HTTPException:
            await ctx.reply("Não foi possível banir o membro.")
        else:
            await ctx.reply(f"`{member}` foi banido com sucesso.")


async def setup(bot: Myu) -> None:
    await bot.add_cog(Moderation(bot))
