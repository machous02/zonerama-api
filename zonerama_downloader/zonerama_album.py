from zonerama_downloader.zonerama_folder import ZoneramaFolder
from zonerama_downloader.zon


class ZoneramaAlbum:
    AlbumId = str
    SecretId = str

    folder: ZoneramaFolder | None
    id: AlbumId
    secret_id: SecretId | None

    def __init__(
        self,
        id: AlbumId,
        folder: ZoneramaFolder | None = None,
        secret_id: SecretId | None = None,
    ):
        self.id = id
        self.folder = folder
        self.secret_id = secret_id

