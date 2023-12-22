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

from typing import TYPE_CHECKING, Any

from discord import Message
from discord.ext.commands import Context

from bot.utils.embed import generate_embed

if TYPE_CHECKING:
    from bot.core import Myu
else:
    Myu = Any


class MyuContext(Context[Myu]):
    """A custom context class for the bot."""

    async def reply(
        self, content: str | None = None, **kwargs: Any
    ) -> Message:
        embed = generate_embed(content, member=self.author)
        return await super().reply(embed=embed, mention_author=False, **kwargs)
