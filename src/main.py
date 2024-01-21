import asyncio
import logging

from app import start_pathfinder
from core.config import settings


def callback(changes):
    logging.debug('changes detected', changes)


def main():
    asyncio.run(start_pathfinder())


if __name__ == "__main__":
    if settings.debug:
        from watchfiles import run_process

        run_process('.', target=main, callback=callback)
    else:
        main()
