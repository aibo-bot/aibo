import sys
import asyncio
import logging

import asyncpg
import aiohttp

import config
from bot import BotBase
from helpers.logging import ColourHandler


level = logging.INFO
logging.basicConfig(level=level, handlers=[ColourHandler(level)])

async def launch():
    min_size, max_size = config.POSTGRES_SIZE
    pool = await asyncpg.create_pool(
        config.POSTGRES_DSN,
        min_size=min_size,
        max_size=max_size
    )
    session = aiohttp.ClientSession()

    assert pool is not None

    resync = "--sync" in sys.argv
    bot = BotBase(pool, session, resync=resync)

    async with bot:
        await bot.start(config.TOKEN)

loop = asyncio.new_event_loop()
loop.run_until_complete(launch())