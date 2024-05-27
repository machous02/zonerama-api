class ZoneramaAndroidException(Exception):
    pass


class ZoneramaAndroidNotLoggedInException(ZoneramaAndroidException):
    pass


class ZoneramaAndroidInvalidLoginException(ZoneramaAndroidException):
    pass


class ZoneramaAndroidWrongPasswordException(ZoneramaAndroidException):
    pass


class ZoneramaAndroidUnknownAccountID(ZoneramaAndroidException):
    pass


class ZoneramaAndroidUnknownTabID(ZoneramaAndroidException):
    pass

class ZoneramaAndroidUnknownAlbumID(ZoneramaAndroidException):
    pass


class ZoneramaAndroidAccessDenied(ZoneramaAndroidException):
    pass
