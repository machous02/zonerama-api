class ZoneramaDownloaderException(Exception):
    pass


class ZipDownloaderException(ZoneramaDownloaderException):
    pass


class InvalidZipIdException(ZipDownloaderException):
    id: str


class UnknownResponseException(ZipDownloaderException):
    response: str


class SecretIdNotSpecifiedException(ZipDownloaderException):
    pass


class ZoneramaApiException(ZoneramaDownloaderException):
    pass


class InvalidZoneramaFolderIdException(ZoneramaApiException):
    id: str


class InvalidZoneramaUsernameException(ZoneramaApiException):
    username: str
