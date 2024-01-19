import logging

from core.config import settings


async def start_pathfinder():
    logging.debug(f"Server started. Listening on port {settings.port}")
