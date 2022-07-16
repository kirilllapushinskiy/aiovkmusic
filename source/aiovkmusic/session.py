from .vk_api import AuthError, ApiError, Captcha, VkApi
from . import audio

from .exceptions import AuthorizationError, AwaitedCaptcha


class VKSession:
    def __init__(self, login: str, password: str, session_file_path: str = 'vk_session.json'):
        """
        Авторизация с получением к vk api - создание сессии.
        :param login: Логин пользователя (телефон, почта).
        :param password: Пароль пользователя вконтакте.
        :param session_file_path: Путь к файлу для сохранения сессии.
        """
        VkApi.RPS_DELAY = 0
        try:
            self._vk_session = VkApi(
                login=login,
                password=password,
                config_filename=session_file_path
            )
            self._vk_session.auth(token_only=True)
        except AuthError as err:
            raise AuthorizationError() from err
        except Captcha:
            raise AwaitedCaptcha()
        try:
            audio.RPS_DELAY_RELOAD_AUDIO = 0
            audio.RPS_DELAY_LOAD_SECTION = 0
            audio.TRACKS_PER_USER_PAGE = 1000
            audio.TRACKS_PER_ALBUM_PAGE = 1000
            audio.ALBUMS_PER_USER_PAGE = 100
            self.__vk_audio = audio.VkAudio(vk=self._vk_session)
        except ApiError as err:
            raise AuthorizationError() from err

    @property
    def api(self) -> VkApi:
        return self._vk_session

    @property
    def audio(self) -> audio.VkAudio:
        return self.__vk_audio
