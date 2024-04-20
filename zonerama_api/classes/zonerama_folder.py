from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_api.classes.zonerama_gallery import ZoneramaGallery

from zonerama_api.z_typing import FolderId, SecretId, FolderPassword
from zonerama_api.api import get_folder_albums, get_folder_name
from zonerama_api.classes.zonerama_album import ZoneramaAlbum


class ZoneramaFolder:
    """A class representing a folder (a tab) in a user's Zonerama Web Gallery."""

    gallery: ZoneramaGallery
    id: FolderId
    secret_id: SecretId | None
    password: FolderPassword | None

    def __init__(
        self,
        gallery: ZoneramaGallery,
        id: FolderId,
        secret_id: SecretId | None = None,
        password: FolderPassword | None = None,
    ):
        self.gallery = gallery
        self.id = id
        self.secret_id = secret_id
        self.password = password

    def get_name(self) -> str:
        return get_folder_name(self.gallery.user.username, self.id)

    @property
    def name(self) -> str:
        return self.get_name()

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
            for id in get_folder_albums(self.id, self.secret_id, self.password)
        ]

    @property
    def albums(self) -> list[ZoneramaAlbum]:
        """A list of albums in the folder sorted as they would appear \
            from top left to bottom right on the web.
        """
        return self.get_albums()
