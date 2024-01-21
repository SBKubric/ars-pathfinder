import logging
import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings

from core import enums


class Settings(BaseSettings):
    project_name: str = 'ARS Pathfinder'
    host: str = '127.0.0.1'
    port: int = 50051

    # Redis
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cache_ttl: int = 60
    redis_server_state_key: str = 'server_state'
    state_storage: str = enums.StateStorage.REDIS

    # Shortest path algorithm setting
    algo: str = enums.AlgoValues.ASTAR_MANHATTAN
    pool_size: int = 1

    # Корень проекта
    base_dir: str = os.path.dirname(os.path.dirname(__file__))

    log_level: str = "INFO"

    sentry_dsn_auth: SecretStr = SecretStr("")
    debug: bool = False

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}"


settings = Settings()  # type: ignore

if settings.sentry_dsn_auth:
    import sentry_sdk  # type: ignore

    sentry_sdk.init(
        dsn=settings.sentry_dsn_auth.get_secret_value(), traces_sample_rate=1.0
    )


# Set up logging
logging.basicConfig(level=settings.log_level)
