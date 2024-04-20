from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_api.classes.zonerama_album import ZoneramaAlbum

from zonerama_api.classes.zonerama_folder import ZoneramaFolder
from zonerama_api.classes.zonerama_user import ZoneramaUser
from zonerama_api.gallery import GalleryInfo, get_gallery_info, get_user_public_folders
from zonerama_api.typing import UserIdentifier


class ZoneramaGallery:
    """A class representing a user's Zonerama Web Gallery."""

    user: ZoneramaUser
    info: GalleryInfo

    def __init__(self, identifier: UserIdentifier):
        self.user = ZoneramaUser(identifier)
        self.refresh_info()

    def refresh_info(self) -> None:
        self.info = get_gallery_info(self.user.username)

    @property
    def name(self) -> str:
        return self.info.name

    @property
    def description(self) -> str:
        return self.info.description

    @property
    def public_folders(self) -> list[ZoneramaFolder]:
        """A list of public folders in the gallery. \
            The list is sorted as it appears left-to-right on the webpage.
        """
        return self._get_public_folders()

    @property
    def public_albums(self) -> list[ZoneramaAlbum]:
        """A list of albums in public folders in the gallery."""
        return self._get_public_albums()

    def _get_public_folders(self) -> list[ZoneramaFolder]:
        """Get all public folders (tabs) in the users gallery. \
            The list is sorted as it appears left-to-right on the webpage.

        Returns:
            list[ZoneramaFolder]: A list of objects representing folders in the users gallery.
        """
        return [
            ZoneramaFolder(id, gallery=self)
            for id in get_user_public_folders(self.user.username)
        ]

    def _get_public_albums(self) -> list[ZoneramaAlbum]:
        """Get all albums in public folders in the user's gallery.

        Returns:
            list[ZoneramaAlbum]: A list of objects representing albums in the users gallery.
        """
        result: list[ZoneramaAlbum] = []
        for folder in self.public_folders:
            result += folder.albums
        return result
