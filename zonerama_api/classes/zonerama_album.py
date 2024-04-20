from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_api.classes.zonerama_folder import ZoneramaFolder

from functools import cached_property

from zonerama_api.album import (
    AlbumInfo,
    download_album,
    get_album_info,
    get_album_photos,
)
from zonerama_api.classes.zonerama_photo import ZoneramaPhoto
from zonerama_api.typing import AlbumId, SecretId


class ZoneramaAlbum:
    """A class representing an album in the Zonerama Web Gallery."""

    id: AlbumId
    folder: ZoneramaFolder | None
    secret_id: SecretId | None
    info: AlbumInfo

    def __init__(
        self,
        id: AlbumId,
        folder: ZoneramaFolder | None = None,
        secret_id: SecretId | None = None,
    ):
        self.id = id
        self.folder = folder
        self.secret_id = secret_id
        self.refresh_info()

    def refresh_info(self) -> None:
        self.info = get_album_info(self.id, self.secret_id)

    @property
    def name(self) -> str:
        return self.info.name

    @property
    def photo_count(self) -> int:
        return self.info.size.photo_count

    @property
    def video_count(self) -> int:
        return self.info.size.video_count

    @property
    def zip_size(self) -> int:
        return self.info.size.zip_size

    @cached_property
    def photos(self) -> list[ZoneramaPhoto]:
        return self._get_photos()

    def _get_photos(self) -> list[ZoneramaPhoto]:
        return [ZoneramaPhoto(photo_id, self) for photo_id in get_album_photos(self.id)]

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
            av1 (bool, optional): Whether the av1 codec should be preferred when available. Defaults to False.
            raw (bool, optional): Whether raw files should be included when available. Defaults to False.
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
