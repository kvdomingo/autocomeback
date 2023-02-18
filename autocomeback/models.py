from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Comeback(BaseModel):
    date: datetime
    artist: str
    release: str
    album_title: str
    song_title: Optional[str]
    album_type: Optional[str]
    artist_type: str
