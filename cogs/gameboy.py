from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from helpers.views.gameboy import PyBoyView
from helpers.fmt import warning_message

if TYPE_CHECKING:
    from bot import BotBase


class Gameboy(commands.GroupCog, description="Emulate a gameboy with classic retro games"):
    def __init__(self, bot: BotBase):
        self.bot = bot

    @app_commands.command(
        description="Boot up a gameboy game. We currently only have Pokemon red!"
    )
    async def start(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)

        view = PyBoyView("assets/roms/pokemonred.gb", interaction.user)
        embed, file = await view.render_screen() # type: ignore
        await interaction.followup.send(view=view, embed=embed, file=file, ephemeral=False)

        timed_out = await view.wait()
        if timed_out:
            view.boy.stop(save=False)

            await interaction.edit_original_message(
                content=warning_message((
                    "No one appears to be using this gameboy anymore. "
                    "I've gone ahead and destroyed the gameboy to save valuable power!"
                )),
                embed=None,
                attachments=[],
                view=None
            )

    
async def setup(bot: BotBase):
    await bot.add_cog(Gameboy(bot))