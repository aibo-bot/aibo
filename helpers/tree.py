from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

from discord import app_commands

from .sentry import capture_sentry
from .fmt import error_message

if TYPE_CHECKING:
    from discord.app_commands import AppCommandError
    from discord import Interaction


class CustomTree(app_commands.CommandTree):
    async def on_error(self, interaction: Interaction, error: AppCommandError) -> None:
        traceback.print_exception(type(error), error, error.__traceback__)
        await capture_sentry(error)

        msg = error_message(
            "Unfortunately something went wrong. "
            "The error has been tracked and we'll be right on to fix it!"
        )

        meth = interaction.followup.send if interaction.response.is_done() else interaction.response.send_message
        await meth(content=msg)