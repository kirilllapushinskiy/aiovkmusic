from vk_api import audio, VkApi
from vk_api.exceptions import AuthError, ApiError, Captcha

from .exceptions import AuthorizationError, AwaitedCaptcha


class VKSession:
    def __init__(self, login: str, password: str, session_file_path: str = 'vk_session.json'):
        """
        Авторизация с получением к vk api - создание сессии.
        :param login: Логин пользователя (телефон, почта).
        :param password: Пароль пользователя вконтакте.
        :param session_file_path: Путь к файлу для сохранения сессии.
        """
        try:
            self.__vk_session = VkApi(
                login=login,
                password=password,
                config_filename=session_file_path
            )
            self.__vk_session.auth(token_only=True)
        except AuthError as err:
            raise AuthorizationError() from err
        except Captcha:
            raise AwaitedCaptcha()
        try:
            self.__vk_audio = audio.VkAudio(self.__vk_session)
        except ApiError as err:
            raise AuthorizationError() from err

    @property
    def api(self) -> VkApi:
        return self.__vk_session

    @property
    def audio(self) -> audio.VkAudio:
        return self.__vk_audio
