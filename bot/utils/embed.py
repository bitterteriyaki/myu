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

from discord import Embed
from discord.abc import User

EMBED_COLOR = 0x5300C4


def generate_embed(
    content: str | None = None, /, *, member: User | None = None
) -> Embed:
    embed = Embed(description=content, color=EMBED_COLOR)

    if member is not None:
        icon_url = member.display_avatar.url
        embed.set_author(name=member.display_name, icon_url=icon_url)

    return embed
