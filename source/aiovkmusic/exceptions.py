TWOFACTOR_CODE = -2
HTTP_ERROR_CODE = -1
TOO_MANY_RPS_CODE = 6
CAPTCHA_ERROR_CODE = 14
NEED_VALIDATION_CODE = 17


class VkApiError(Exception):
    pass


class AccessDenied(VkApiError):
    pass


class AuthError(VkApiError):
    pass


class LoginRequired(AuthError):
    pass


class PasswordRequired(AuthError):
    pass


class BadPassword(AuthError):
    pass


class AccountBlocked(AuthError):
    pass


class TwoFactorError(AuthError):
    pass


class SecurityCheck(AuthError):

    def __init__(self, phone_prefix=None, phone_postfix=None, response=None):
        super(SecurityCheck, self).__init__()

        self.phone_prefix = phone_prefix
        self.phone_postfix = phone_postfix
        self.response = response

    def __str__(self):
        if self.phone_prefix and self.phone_postfix:
            return 'Security check. Enter number: {} ... {}'.format(
                self.phone_prefix, self.phone_postfix
            )
        else:
            return ('Security check. Phone prefix and postfix are not detected.'
                    ' Please send bugreport (response in self.response)')


class ApiError(VkApiError):

    def __init__(self, vk, method, values, raw, error):
        super(ApiError, self).__init__()

        self.vk = vk
        self.method = method
        self.values = values
        self.raw = raw
        self.code = error['error_code']
        self.error = error

    def try_method(self):
        """ Отправить запрос заново """

        return self.vk.method(self.method, self.values, raw=self.raw)

    def __str__(self):
        return '[{}] {}'.format(self.error['error_code'],
                                self.error['error_msg'])


class ApiHttpError(VkApiError):

    def __init__(self, vk, method, values, raw, response):
        super(ApiHttpError, self).__init__()

        self.vk = vk
        self.method = method
        self.values = values
        self.raw = raw
        self.response = response

    def try_method(self):
        """ Отправить запрос заново """

        return self.vk.method(self.method, self.values, raw=self.raw)

    def __str__(self):
        return 'Response code {}'.format(self.response.status_code)


class Captcha(VkApiError):

    def __init__(self, vk, captcha_sid, func, args=None, kwargs=None, url=None):
        super(Captcha, self).__init__()

        self.vk = vk
        self.sid = captcha_sid
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}

        self.code = CAPTCHA_ERROR_CODE

        self.key = None
        self.url = url
        self.image = None

    def get_url(self):
        """ Получить ссылку на изображение капчи """

        if not self.url:
            self.url = 'https://api.vk.com/captcha.php?sid={}'.format(self.sid)

        return self.url

    def get_image(self):
        """ Получить изображение капчи (jpg) """

        if not self.image:
            self.image = self.vk.http.get(self.get_url()).content

        return self.image

    def try_again(self, key=None):
        """ Отправить запрос заново с ответом капчи

        :param key: ответ капчи
        """

        if key:
            self.key = key

            self.kwargs.update({
                'captcha_sid': self.sid,
                'captcha_key': self.key
            })

        return self.func(*self.args, **self.kwargs)

    def __str__(self):
        return 'Captcha needed'


class VkAudioException(Exception):
    pass


class VkAudioUrlDecodeError(VkAudioException):
    pass


class VkToolsException(VkApiError):
    def __init__(self, *args, response=None):
        super().__init__(*args)
        self.response = response


class VkRequestsPoolException(Exception):
    def __init__(self, error, *args, **kwargs):
        self.error = error
        super(VkRequestsPoolException, self).__init__(*args, **kwargs)


class PlaylistsAccessDenied(Exception):
    def __init__(self, owner_id):
        self.message = f'У вас не прав доступа для просмотра плейлистов данного пользователя ({owner_id}).'

    def __str__(self):
        return self.message


class TracksAccessDenied(Exception):
    def __init__(self, owner_id):
        self.message = f'У вас не прав доступа для просмотра аудиозаписей данного пользователя ({owner_id}).'

    def __str__(self):
        return self.message


class NonExistentUser(Exception):
    def __init__(self, username):
        self.message = f"Пользователь с {'id' if username.isdigit() else 'логином'}: {username} - не найден."

    def __str__(self):
        return self.message


class InvalidBitrate(Exception):
    def __init__(self, bitrate):
        self.message = f"Недопустимый битрейт: {bitrate}kb."

    def __str__(self):
        return self.message


class AuthorizationError(Exception):
    def __init__(self):
        self.message = f"Ошибка авторизации. Возможно введён неверный логин или пароль."

    def __str__(self):
        return self.message


class AwaitedCaptcha(AuthorizationError):
    def __init__(self):
        self.message = f"Ожидается ввод капчи. Попробуйте авторизоваться попозже"

    def __str__(self):
        return self.message
