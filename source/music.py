import asyncio
from pathlib import PurePath

from ffmpeg import FFmpeg

from .exceptions import PlaylistsAccessDenied, NonExistentUser, InvalidBitrate
from .model import Track, Playlist
from .session import VKSession
from vk_api.exceptions import AuthError, AccessDenied


class Music:
    def __init__(self, user: str, session: VKSession):
        """

        :param user:
        :param session:
        """
        self._api = session.api
        self._audio = session.audio
        if user.isdigit():
            self._user_id = user
        else:
            object_info = self._api.method(
                'utils.resolveScreenName', {'screen_name': user}
            )
            if not object_info:
                raise NonExistentUser(user)
            self._user_id = object_info['object_id']
        self._user_info = self._api.method("users.get", {"user_ids": self._user_id})

    def playlists(self, owner_id: int) -> [Playlist]:
        """

        :param owner_id:
        :return:
        """
        try:
            albums = self._audio.get_albums(owner_id, )
        except AccessDenied:
            raise PlaylistsAccessDenied(owner_id)
        return [
            Playlist(
                id=album['id'],
                owner_id=album['owner_id'],
                url=album['url'],
                plays=album['plays'],
                title=album['title'],
                access_hash=album['access_hash']
            )
            for album in albums
        ]

    def search(self, text: str, count: int = 5, offset: int = 0, official=False) -> [Track]:
        """

        :param text:
        :param count:
        :param offset:
        :param official:
        :return:
        """
        tracks = self._audio.search(q=text, count=100 + count, offset=offset)
        if official:
            tracks = list(filter(lambda t: t['owner_id'] < 0, tracks))[0:count]
        return [
            Track(
                id=track['id'],
                owner_id=track['owner_id'],
                duration=track['duration'],
                url=track['url'],
                _covers=track['track_covers'],
                artist=track['artist'],
                title=track['title']
            )
            for track in tracks
        ]

    def search_generator(self, text: str, step: int = 5, count: int = 25, official=False) -> iter:
        """

        :param text:
        :param step:
        :param count:
        :param official:
        :return:
        """
        tracks = self.search(text=text, count=count, official=official)
        _start, _step = 0, step
        while _start < len(tracks):
            yield tracks[_start:_start + _step]
            _start += _step

    def track(self, owner_id: int, track_id: int) -> Track:
        """

        :param owner_id:
        :param track_id:
        :return:
        """
        track = self._audio.get_audio_by_id(owner_id=owner_id, audio_id=track_id)
        return Track(
            id=track['id'],
            owner_id=track['owner_id'],
            duration=track['duration'],
            url=track['url'],
            _covers=track['track_covers'],
            artist=track['artist'],
            title=track['title']
        )

    def album_tracks(self, album: Playlist) -> [Track]:
        """

        :param album:
        :return:
        """
        tracks = self._audio.get(
            album_id=album.id,
            owner_id=album.owner_id,
            access_hash=album.access_hash
        )
        return [
            Track(
                id=track['id'],
                owner_id=track['owner_id'],
                duration=track['duration'],
                url=track['url'],
                _covers=track['track_covers'],
                artist=track['artist'],
                title=track['title']
            )
            for track in tracks
        ]

    async def download(
            self,
            *tracks: Track,
            count: int = 5,
            offset: int = 0,
            path: str = './',
            bitrate: int = 320
    ) -> [Track]:
        """

        :param tracks:
        :param count:
        :param offset:
        :param path:
        :param bitrate:
        :return:
        """
        to_download = []
        _tracks = tracks[0] if len(tracks) == 1 and isinstance(tracks[0], list | tuple) else tracks
        for track in _tracks[offset:count + offset]:
            track.path = str(PurePath(path, track.fullname + '.mp3'))
            to_download.append(self._downloader(track.url, track.path, bitrate=bitrate))
        await asyncio.gather(*to_download)
        return tracks

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def first_name(self) -> str:
        return self._user_info[0]['first_name']

    @property
    def last_name(self) -> str:
        return self._user_info[0]['first_name']

    @staticmethod
    async def _downloader(url: str, name: str, bitrate: int):
        """

        :param url:
        :param name:
        :param bitrate:
        :return:
        """
        if bitrate not in (320, 192, 256, 128, 160, 6, 32):
            raise InvalidBitrate(bitrate)
        await FFmpeg().option('y').option(
            'http_persistent', 'false'
        ).input(url).output(
            name, {'b:a': f'{bitrate}k'}
        ).execute()
