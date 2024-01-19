import logging
import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = 'ARS Pathfinder'
    port: int = 50051

    # Настройки Redis
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cache_ttl: int = 60

    # Корень проекта
    base_dir: str = os.path.dirname(os.path.dirname(__file__))

    log_level: str = "INFO"

    sentry_dsn_auth: SecretStr = SecretStr("")
    debug: bool = False


settings = Settings()  # type: ignore

if settings.sentry_dsn_auth:
    import sentry_sdk  # type: ignore

    sentry_sdk.init(
        dsn=settings.sentry_dsn_auth.get_secret_value(), traces_sample_rate=1.0
    )


# Set up logging
logging.basicConfig(level=settings.log_level)
