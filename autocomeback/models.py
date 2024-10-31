from datetime import datetime

from pydantic import BaseModel


class Comeback(BaseModel):
    date: datetime
    artist: str
    album_title: str
    release: str | None
    song_title: str | None
    album_type: str | None
    title_track: str | None
    artist_type: str | None
