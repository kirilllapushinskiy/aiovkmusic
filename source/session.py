from vk_api import audio, VkApi
from vk_api.exceptions import AuthError


class VKSession:
    def __init__(self, login: str, password: str, session_file_path: str = 'vk_session.json'):
        try:
            self.__vk_session = VkApi(
                login=login,
                password=password,
                config_filename=session_file_path
            )
            self.__vk_session.auth(token_only=True)
        except AuthError as err:
            print("VKSession error:", err)
        self.__vk_audio = audio.VkAudio(self.__vk_session)

    @property
    def api(self) -> VkApi:
        return self.__vk_session

    @property
    def audio(self) -> audio.VkAudio:
        return self.__vk_audio
