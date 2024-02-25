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
