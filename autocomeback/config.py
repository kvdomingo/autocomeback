from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings, SettingsConfigDict

from autocomeback import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_API_USER_AGENT: str = (
        f"cloudfunctions:autocomeback:v{__version__} (by /u/arockentothemoon)"
    )
    DEFAULT_TZ: ZoneInfo = ZoneInfo("Asia/Seoul")


settings = Settings()
