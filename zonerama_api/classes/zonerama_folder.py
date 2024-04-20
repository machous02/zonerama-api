from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_api.classes.zonerama_gallery import ZoneramaGallery

from zonerama_api.typing import FolderId, SecretId, FolderPassword
from zonerama_api.folder import get_folder_albums, FolderInfo, get_folder_info
from zonerama_api.classes.zonerama_album import ZoneramaAlbum


class ZoneramaFolder:
    """A class representing a folder (a tab) in a user's Zonerama Web Gallery."""

    id: FolderId
    gallery: ZoneramaGallery | None
    secret_id: SecretId | None
    password: FolderPassword | None
    info: FolderInfo | None

    def __init__(
        self,
        id: FolderId,
        gallery: ZoneramaGallery | None = None,
        secret_id: SecretId | None = None,
        password: FolderPassword | None = None,
    ):
        self.id = id
        self.gallery = gallery
        self.secret_id = secret_id
        self.password = password
        if self.gallery is not None:
            self.info = self.refresh_info()

    def refresh_info(self) -> None:
        assert self.gallery is not None
        self.info = get_folder_info(self.gallery.user.username, self.id)

    @property
    def name(self) -> str:
        assert self.info is not None
        return self.info.name

    @property
    def albums(self) -> list[ZoneramaAlbum]:
        """A list of albums in the folder sorted as they would appear \
            from top left to bottom right on the web.
        """
        return self._get_albums()

    def _get_albums(self) -> list[ZoneramaAlbum]:
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
