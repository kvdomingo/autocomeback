from pydantic import BaseSettings
from pytz import timezone

from autocomeback import __version__


class Settings(BaseSettings):
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_API_USER_AGENT: str = (
        f"cloudfunctions:autocomeback:v{__version__} (by /u/arockentothemoon)"
    )
    DEFAULT_TZ = timezone("Asia/Seoul")

    class Config:
        env_file = ".env"


settings = Settings()
