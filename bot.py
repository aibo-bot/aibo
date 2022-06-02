from __future__ import annotations

import logging
import pathlib
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

import config
from helpers.tree import CustomTree

if TYPE_CHECKING:
    from asyncpg import Pool
    from aiohttp import ClientSession


_log = logging.getLogger(__name__)

class BotBase(commands.Bot):
    def __init__(
        self,
        pool: Pool,
        session: ClientSession,
        *,
        resync: bool
    ):
        self.pool: Pool = pool
        self.session: ClientSession = session
        self.config = config

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            command_prefix="games!",
            description="A cool games bot",
            intents=intents,
            tree_cls=CustomTree
        )

        self.__resync_commands = resync

    async def setup_hook(self) -> None:
        for file in pathlib.Path("./cogs").iterdir():
            if file.is_dir():
                continue
            
            ext = "cogs." + file.stem
            await self.load_extension(ext)
            _log.info("Loaded %s", ext)

        # Load jishaku
        await self.load_extension("jishaku")
        _log.info("Loaded jishaku")

        if self.__resync_commands:
            _log.info("Attempting to resync application commands")
            guild = discord.Object(id=config.TESTING_GULD)
            self.tree.copy_global_to(guild=guild)
            
            await self.tree.sync(guild=guild)
            await self.tree.sync()

    async def close(self) -> None:
        await self.session.close()
        await self.pool.close()
        
        return await super().close()
