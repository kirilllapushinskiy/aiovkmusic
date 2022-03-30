from dataclasses import dataclass, field


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
    cover_url: str | None = field(init=False)
    url: str
    artist: str
    title: str
    duration: int
    _covers: [str] = field(repr=False)
    path: str = field(default=None, init=False)

    def __post_init__(self):
        self.cover_url = self._covers.pop() if len(self._covers) > 0 else None
        self.title = self._clear_str(self.title)
        self.artist = self._clear_str(self.artist)
        self.fullname = self.title + ' - ' + self.artist

    @staticmethod
    def _clear_str(string):
        return ''.join(c for c in string if c.isalnum() or c in ' -')
