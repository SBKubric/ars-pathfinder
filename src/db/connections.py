import logging

from redis.asyncio import Redis, default_backoff

from core import exceptions as exc
from core.config import settings


class RedisConnector:
    """
    Redis connection manager as context manager object.

    Attributes:
        _connection (Redis): An instance of the Redis class representing the connection to the Redis database.
    """

    def __init__(self):
        """
        Initializes the RedisConnector object. Establishes a connection to the Redis database.

        Raises:
            PathfinderError: If the connection to the Redis database fails.
        """
        self._connection_to_await = Redis.from_url(
            settings.redis_url, retry_on_timeout=True, socket_connect_timeout=10
        )
        self._connection: Redis | None = None

    async def __aenter__(self):
        """
        Returns the Redis connection when entering the context.

        Returns:
            Redis: The Redis connection.
        """
        self._connection = await self._connection_to_await
        is_alive = self._connection.ping()
        if not is_alive:
            raise exc.PathfinderError("Redis connection failed")
        return self._connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Handles cleanup when exiting the context. Logs any errors and closes the Redis connection.

        Parameters:
            exc_type (Type[BaseException]): The type of the exception.
            exc_val (BaseException): The exception instance.
            exc_tb (TracebackType): The traceback object encapsulating the call stack at the point where the exception was raised.
        """
        if exc_type or exc_val or exc_tb:
            logging.error(exc_type, exc_tb, exc_val)
        if not self._connection:
            logging.warning("Redis connection is None")
            return
        await self._connection.aclose()
