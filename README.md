# aiovkmusic

### Описание

> *Python пакет для поиска музыки и плейлистов в VK с возможностью асинхронного скачивания аудиозаписей.*
___

[Что нового в последней версии?](CHANGES.md)

* #### 
  Установка [aiovkmusic](https://pypi.org/project/aiovkmusic/) средствами [PyPi](https://pypi.org/): `pip install aiovkmusic`
* #### И убедитесь, что на ваш компьютер установлен [ffmpeg](https://ffmpeg.org/download.html).

___
Сразу же перейдём к примерам использования:

```python
import asyncio
from aiovkmusic import Music, VKSession, Track, Playlist


async def main():
    # Создание сессии.
    # ВАЖНО: подключаемый аккаунт ВК должен быть БЕЗ двухэтапной аутентификации.
    # (Если переживаете - используйте фейк.)
    session = VKSession(
        login='<номер_телефона/электронная_почта>',
        password='<пароль_от_вконтакте>',
        session_file_path='session.json'
    )

    # Получение интерфейса к vk music api.
    music = Music(user='<ссылка_на_профиль>', session=session)

    # Получение всех плейлистов указанного пользователя.
    playlists = music.playlists()  # -> [Playlists]

    for playlist in playlists:
        print(playlist.title)

    # pyrokinesis
    # GAME OVER
    # Live Rock

    # Получение аудиозаписей указанного плейлиста.
    playlist_tracks = music.playlist_tracks(playlists[0])  # -> [Track]

    for track in playlist_tracks:
        print(track.fullname)

    # 99 Problems - Big Baby Tape kizaru
    # So Icy Nihao - Big Baby Tape kizaru
    # Big Tymers - Big Baby Tape kizaru

    # Поиск по названию (аналогично поиску в VK).
    tracks = music.search('Три дня дождя', count=5, offset=0, official=True)  # -> [Track]

    for track in tracks:
        print(track.fullname)

    # Вина - Три дня дождя
    # Демоны - Три дня дождя
    # Привычка - Три дня дождя
    # Не выводи меня - МУККА Три дня дождя
    # Не Киряй - МУККА Три дня дождя

    # Загрузка переданных аудиозаписей по указанному пути.
    downloaded_tracks = await music.download(tracks, bitrate=320, path='music')  # -> [Track]

    for track in downloaded_tracks:
        print(track.path)

    # music/108481371.mp3
    # music/62163423.mp3
    # music/106817510.mp3
    # music/60284123.mp3
    # music/105514252.mp3

    #
    # <--- NEW IN VERSION 1.1.0! --->
    # 

    # Получение аудиозаписей указанного пользователя.
    user_tracks = music.user_tracks()  # -> [Track]


asyncio.run(main())
```

Используемые представления данных:

```python
class Playlist:
    id: int
    owner_id: int
    title: str
    plays: int
    url: str
    access_hash: str


class Track:
    id: int
    owner_id: int
    cover_url: str
    url: str
    artist: str
    title: str
    duration: int
    path: str
    fullname: str
```

___

#### How to contact the maintainer:

![](https://img.shields.io/badge/telegram-Kirill_Lapushinskiy-blue?style=social&logo=telegram&link=https://t.me/kirilllapushinskiy)

![](https://img.shields.io/badge/VK-Kirill_Lapushinskiy-blue?style=social&logo=vk&link=https://vk.com/kirilllapushinskiy)
