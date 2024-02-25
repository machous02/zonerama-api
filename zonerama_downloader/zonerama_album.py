from zonerama_downloader.zonerama_folder import ZoneramaFolder
from zonerama_downloader.download_album import download_album


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

    def download(
        self,
        destination_folder: str,
        include_videos: bool = True,
        original: bool = False,
        av1: bool = False,
        raw: bool = False,
        sleep_for: float = 5.0,
    ) -> None:
        download_album(
            self, include_videos, original, av1, raw, destination_folder, sleep_for
        )
