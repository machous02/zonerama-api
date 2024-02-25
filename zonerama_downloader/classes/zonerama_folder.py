from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_downloader.classes.zonerama_gallery import ZoneramaGallery

from zonerama_downloader.zonerama_api import get_user_folder_albums
from zonerama_downloader.classes.zonerama_album import ZoneramaAlbum


class ZoneramaFolder:
    """A class representing a folder (a tab) in a user's Zonerama Web Gallery."""

    FolderId = str
    SecretFolderId = str

    gallery: ZoneramaGallery
    id: FolderId
    secret_id: SecretFolderId | None

    def __init__(
        self,
        gallery: ZoneramaGallery,
        id: FolderId,
        secret_id: SecretFolderId | None = None,
    ):
        self.gallery = gallery
        self.id = id
        self.secret_id = secret_id

    def get_albums(self) -> list[ZoneramaAlbum]:
        """Returns a list of albums in the folder. \
            The list is sorted as it would appear \
            from top left to bottom right on the web.

        Returns:
            list[ZoneramaAlbum]: A list of album objects representing albums in the folder. \
                                 The list is sorted in the aforementioned order.
        """
        return [
            ZoneramaAlbum(id, self, self.secret_id)
            for id in get_user_folder_albums(self.gallery.username, self.id, self.secret_id)
        ]

    @property
    def albums(self) -> list[ZoneramaAlbum]:
        """A list of albums in the folder sorted as they would appear \
            from top left to bottom right on the web.
        """
        return self.get_albums()
