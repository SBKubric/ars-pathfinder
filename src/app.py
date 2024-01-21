import concurrent.futures as cf
import logging

from grpclib.reflection.service import ServerReflection
from grpclib.server import Server
from grpclib.utils import graceful_exit

from core.config import settings
from db.connections import RedisConnector
from server.handlers import Pathfinder
from state.state import get_state


async def start_pathfinder():
    """
    Start the server and listen for incoming requests. Search algorithm is run inside separate process pool.
    """
    with cf.ProcessPoolExecutor(max_workers=settings.pool_size) as executor:
        async with RedisConnector() as connection:
            state = get_state(connection)
            services = ServerReflection.extend([Pathfinder(executor, state)])
            server = Server(services)
            with graceful_exit([server]):
                await server.start(port=settings.port)
                logging.debug(
                    f"Server started. Listening on host {settings.host} and port {settings.port}"
                )
                await server.wait_closed()
