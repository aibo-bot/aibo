from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import BotBase


async def setup(bot: BotBase):
    ...
