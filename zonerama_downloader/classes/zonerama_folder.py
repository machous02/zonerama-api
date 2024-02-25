from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_downloader.classes.zonerama_gallery import ZoneramaGallery

from zonerama_downloader.zonerama_api import get_user_folder_public_albums
from zonerama_downloader.classes.zonerama_album import ZoneramaAlbum


class ZoneramaFolder:
    """A class representing a folder (a tab) in a user's Zonerama Web Gallery.
    """
    FolderId = str

    gallery: ZoneramaGallery
    id: FolderId

    def __init__(self, gallery: ZoneramaGallery, id: FolderId):
        self.gallery = gallery
        self.id = id

    def get_albums(self) -> list[ZoneramaAlbum]:
        """Returns a list of albums in the folder. \
            The list is sorted as it would appear \
            from top left to bottom right on the web.

        Returns:
            list[ZoneramaAlbum]: A list of album objects representing albums in the folder. \
                                 The list is sorted in the aforementioned order.
        """
        return [
            ZoneramaAlbum(id, self, None)
            for id in get_user_folder_public_albums(self.gallery.username, self.id)
        ]

    @property
    def albums(self) -> list[ZoneramaAlbum]:
        """A list of albums in the folder sorted as they would appear \
            from top left to bottom right on the web.
        """
        return self.get_albums()
