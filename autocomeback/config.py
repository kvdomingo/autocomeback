from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings, SettingsConfigDict

from autocomeback import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    BASE_DIR: Path = Path(__file__).parent.parent
    DEFAULT_TZ: ZoneInfo = ZoneInfo("Asia/Seoul")

    REDDIT_API_USER_AGENT: str = (
        f"cloudfunctions:autocomeback:v{__version__} (by /u/arockentothemoon)"
    )
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str


@lru_cache
def _get_settings():
    return Settings()


settings = _get_settings()
