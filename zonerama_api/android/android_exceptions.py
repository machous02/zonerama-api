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


class ZoneramaAndroidAccessDenied(ZoneramaAndroidException):
    pass
