import logging
from abc import ABC, abstractmethod
from functools import cache
from typing import Any

import orjson as json
from redis.asyncio import Redis

from core.config import settings
from core.enums import StateStorage
from core.exceptions import PathfinderError
from models import Entry


class BaseStorage(ABC):
    """Abstract base class for state storage.

    This class defines the interface for all concrete storage classes. It includes methods for saving and retrieving state.
    """

    @abstractmethod
    async def save_state(self, state: dict[str, Any]):
        """Abstract method for saving state.

        Args:
            state (dict[str, Any]): The state to be saved.
        """
        ...

    @abstractmethod
    async def retrieve_state(self) -> dict[str, Any]:
        """Abstract method for retrieving state.

        Returns:
            dict[str, Any]: The retrieved state.
        """
        ...


class RedisStorage(BaseStorage):
    """Concrete storage class for Redis.

    This class implements the BaseStorage interface using Redis for state storage.
    """

    def __init__(self, connection: Redis):
        """Initialize the RedisStorage instance.

        Args:
            connection (Redis): The Redis connection.
        """
        self.redis = connection

    async def save_state(self, state: dict[str, Any]):
        """Save state to Redis.

        Args:
            state (dict[str, Any]): The state to be saved.
        """
        serialized = json.dumps(state)
        await self.redis.set(settings.redis_server_state_key, serialized)

    async def retrieve_state(self) -> dict[str, Any]:
        """Retrieve state from Redis.

        Returns:
            dict[str, Any]: The retrieved state.
        """
        serialized = await self.redis.get(settings.redis_server_state_key)
        if not serialized:
            return {}
        return json.loads(serialized)


class State:
    """Class for managing state.

    This class provides methods for setting and getting state using a specified storage backend.
    """

    def __init__(self, storage: BaseStorage):
        """Initialize the State instance.

        Args:
            storage (BaseStorage): The storage backend.
        """
        self.storage = storage

    async def set_state(self, value: Entry, key: str = 'robot_id'):
        """Set state.

        Args:
            value (Entry): The state value.
            key (str, optional): The state key. Defaults to 'robot_id'.
        """
        state = await self.storage.retrieve_state()
        state[key] = value.model_dump_json()
        await self.storage.save_state(state)

    async def get_state(self, key: str = 'robot_id') -> Entry | None:
        """Get state.

        Args:
            key (str, optional): The state key. Defaults to 'robot_id'.

        Returns:
            Entry | None: The retrieved state value, or None if the key does not exist.
        """
        state = await self.storage.retrieve_state()
        value = state.get(key)
        if not value:
            return None

        model_dict = json.loads(value)
        return Entry(**model_dict)


def get_state(connection: Redis) -> State:
    """Get a State instance.

    This function returns a State instance configured with the appropriate storage backend based on the application settings.

    Args:
        connection (Redis): The Redis connection.

    Returns:
        State: The State instance.

    Raises:
        PathfinderError: If the state storage mode is unknown.
    """
    if settings.state_storage == StateStorage.REDIS:
        return State(RedisStorage(connection))
    message = f'Unknown state mode: {settings.state_storage}'
    logging.error(f'Unknown state mode: {settings.state_storage}')
    raise PathfinderError(message)
