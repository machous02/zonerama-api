class ZoneramaDownloaderException(Exception):
    pass


class ZipDownloaderException(ZoneramaDownloaderException):
    pass


class InvalidZipIdException(ZipDownloaderException):
    id: str
    message: str | None


class InvalidPhotoIdException(ZipDownloaderException):
    id: str


class UnknownResponseException(ZipDownloaderException):
    response: str


class SecretIdNotSpecifiedException(ZipDownloaderException):
    pass


class ZoneramaApiException(ZoneramaDownloaderException):
    pass


class InvalidZoneramaFolderIdException(ZoneramaApiException):
    """Invalid folder id or secret id.
    """
    folder_id: str
    secret_id: str | None


class InvalidZoneramaUsernameException(ZoneramaApiException):
    username: str
