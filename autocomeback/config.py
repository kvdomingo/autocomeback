from zoneinfo import ZoneInfo

from pydantic import BaseSettings

from autocomeback import __version__


class Settings(BaseSettings):
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_API_USER_AGENT: str = (
        f"cloudfunctions:autocomeback:v{__version__} (by /u/arockentothemoon)"
    )
    DEFAULT_TZ = ZoneInfo("Asia/Seoul")

    class Config:
        env_file = ".env"


settings = Settings()
