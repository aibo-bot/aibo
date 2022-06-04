from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from helpers.fmt import (
    error_message,
    success_message,
    warning_message
)
from helpers.postgres import AccountExists
from helpers.imagemanip.common import save_avatar
from helpers.imagemanip.accounts import generate_account_image

if TYPE_CHECKING:
    from bot import BotBase


class Accounts(commands.GroupCog):
    def __init__(self, bot: BotBase):
        self.bot = bot

    @app_commands.command(
        description="View someone's account information"
    )
    async def view(self, interaction: discord.Interaction, member: discord.Member | None):
        member = member or interaction.user # type: ignore
        
        await interaction.response.defer(ephemeral=True)
        account = await self.bot.postgres.get_account(member.id) # type: ignore

        if account is None:
            return await interaction.followup.send(
                error_message(f"{member} does not have an account."),
                ephemeral=True
            )

        avatar = await save_avatar(member) # type: ignore
        image = await generate_account_image(
            member.name, # type: ignore
            account,
            avatar
        )

        file = discord.File(image, filename="profile.png")
        await interaction.followup.send(
            file=file,
            ephemeral=True
        )

    @app_commands.command(
        description="Create an aibo account"
    )
    async def new(self, interaction: discord.Interaction):
        try:
            await self.bot.postgres.create_account(interaction.user.id)
        except AccountExists:
            await interaction.response.send_message(
                error_message("You already have an account. There's no need to make a new one!"),
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                success_message("Account successfully created. Run `/accounts view` to view your account info!"),
                ephemeral=True
            )

    @app_commands.command(
        description="Edit your aibo about me"
    )
    async def aboutme(self, interaction: discord.Interaction, description: str):
        if len(description) > 50:
            return await interaction.response.send_message(
                error_message("About me's must be 50 characters or less long."),
                ephemeral=True
            )

        account = await self.bot.postgres.get_account(interaction.user.id)

        if account is None:
            return await interaction.response.send_message(
                error_message("You don't have an aibo account. Make one with the `/accounts new` command!"),
                ephemeral=True
            )

        if account.description == description:
            return await interaction.response.send_message(
                warning_message("Your new about me matches your old one. We have not changed your about me."),
                ephemeral=True
            )

        await self.bot.postgres.update_account(
            interaction.user.id,
            description=description
        )

        await interaction.response.send_message(
            success_message("About me successfully updated"),
            ephemeral=True
        )
        
async def setup(bot: BotBase):
    await bot.add_cog(Accounts(bot))
