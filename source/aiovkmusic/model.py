from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Playlist:
    id: int
    owner_id: int
    title: str
    plays: int
    url: str
    access_hash: str


@dataclass
class Track:
    id: int
    owner_id: int
    cover_url: Optional[str] = field(init=False)
    url: str
    artist: str
    title: str
    duration: int
    _covers: [str] = field(repr=False)
    path: Optional[str] = field(default=None, init=False)

    def __post_init__(self):
        self.cover_url = self._covers.pop() if len(self._covers) > 0 else None
        self.fullname = self.title + ' - ' + self.artist
