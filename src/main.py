import asyncio
import logging

from app import start_pathfinder
from core.config import settings


async def callback(changes):
    logging.debug('changes detected', changes)


async def main():
    if settings.debug:
        from watchfiles import arun_process

        await arun_process('.', target=start_pathfinder, callback=callback)
    else:
        await start_pathfinder()


if __name__ == "__main__":
    asyncio.run(main())
