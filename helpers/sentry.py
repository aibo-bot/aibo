import asyncio

import sentry_sdk

import config


sentry_sdk.init(
    config.SENTRY_DSN,
    traces_sample_rate=1.0
)

async def capture_sentry(error: Exception):
    func = sentry_sdk.capture_exception
    await asyncio.to_thread(func, error)
