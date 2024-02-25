from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_downloader.classes.zonerama_folder import ZoneramaFolder

from zonerama_downloader.download_album import download_album


class ZoneramaAlbum:
    """A class representing an album in the Zonerama Web Gallery.
    """
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
        """Downloads the album as a ZIP file. \
            If the author has prohibited downloads, downloads an empty archive.

        Args:
            destination_folder (str): The destination folder for the ZIP file.
            include_videos (bool, optional): Whether videos are included \
                or just their thumbnails. Defaults to True.
            original (bool, optional): Unknown. Defaults to False.
            av1 (bool, optional): Unknown. Defaults to False.
            raw (bool, optional): Unknown. Defaults to False.
            sleep_for (float, optional): The time for which the function sleeps \
                while the file is not ready, in seconds. Defaults to 5.0.
        """
        download_album(
            self.id,
            self.secret_id,
            include_videos,
            original,
            av1,
            raw,
            destination_folder,
            sleep_for,
        )
