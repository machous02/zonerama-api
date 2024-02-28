from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_api.classes.zonerama_album import ZoneramaAlbum

from zonerama_api.zonerama_api import get_user_public_folders
from zonerama_api.classes.zonerama_folder import ZoneramaFolder


class ZoneramaGallery:
    """A class representing a user's Zonerama Web Gallery.
    """
    Username = str

    username: Username

    def __init__(self, username: Username):
        self.username = username

    def get_public_folders(self) -> list[ZoneramaFolder]:
        """Get all public folders (tabs) in the users gallery. \
            The list is sorted as it appears left-to-right on the webpage.

        Returns:
            list[ZoneramaFolder]: A list of objects representing folders in the users gallery.
        """
        return [
            ZoneramaFolder(self, id) for id in get_user_public_folders(self.username)
        ]

    @property
    def public_folders(self) -> list[ZoneramaFolder]:
        """A list of public folders in the gallery. \
            The list is sorted as it appears left-to-right on the webpage.
        """
        return self.get_public_folders()

    def get_public_albums(self) -> list[ZoneramaAlbum]:
        """Get all albums in public folders in the user's gallery.

        Returns:
            list[ZoneramaAlbum]: A list of objects representing albums in the users gallery.
        """
        result: list[ZoneramaAlbum] = []
        for folder in self.public_folders:
            result += folder.albums
        return result

    @property
    def public_albums(self) -> list[ZoneramaAlbum]:
        """A list of albums in public folders in the gallery.
        """
        return self.get_public_albums()
