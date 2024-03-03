from __future__ import annotations

from typing import TYPE_CHECKING
from functools import cached_property

if TYPE_CHECKING:
    from zonerama_api.classes.zonerama_folder import ZoneramaFolder

from zonerama_api.typing import AlbumId, SecretId
from zonerama_api.api import (
    download_album,
    get_album_size,
    get_album_name,
    AlbumSize,
)


class ZoneramaAlbum:
    """A class representing an album in the Zonerama Web Gallery."""

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

    def get_name(self) -> str:
        return get_album_name(self.id)

    @cached_property
    def name(self) -> str:
        return self.get_name()

    def get_size(self, include_videos: bool = True, include_raws: bool = False) -> AlbumSize:
        return get_album_size(self.id, include_videos, include_raws, self.secret_id)

    @cached_property
    def size(self) -> AlbumSize:
        return self.get_size()

    @cached_property
    def size_without_videos(self) -> AlbumSize:
        return self.get_size(include_videos=False)

    @cached_property
    def size_with_raws(self) -> AlbumSize:
        return self.get_size(include_raws=True)

    @property
    def photo_count(self) -> int:
        return self.size.photo_count

    @property
    def video_count(self) -> int:
        return self.size.video_count

    @property
    def zip_size(self) -> int:
        return self.size.zip_size

    @property
    def zip_size_without_videos(self) -> int:
        return self.size_without_videos.zip_size

    @property
    def zip_size_with_raws(self) -> int:
        return self.size_with_raws.zip_size

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
