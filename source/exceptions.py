class PlaylistsAccessDenied(Exception):
    def __init__(self, owner_id):
        self.message = f'У вас не прав доступа для просмотра плейлистов данного пользователя({owner_id}).'

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