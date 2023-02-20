from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Comeback(BaseModel):
    date: datetime
    artist: str
    album_title: str
    release: Optional[str]
    song_title: Optional[str]
    album_type: Optional[str]
    title_track: Optional[str]
    artist_type: Optional[str]
