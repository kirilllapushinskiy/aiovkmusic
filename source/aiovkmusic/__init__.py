import sys
import warnings

import loguru

from .model import Track, Playlist
from .music import Music
from .session import VKSession

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
loguru.logger.remove()
loguru.logger.add(
    sink=sys.stdout,
    format="{level} {time:MMM DD HH:mm:ss.SSS}: {message}",
    enqueue=True
)
