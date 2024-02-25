from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_downloader.classes.zonerama_gallery import ZoneramaGallery
    from zonerama_downloader.classes.zonerama_album import ZoneramaAlbum

from zonerama_downloader.zonerama_api import get_user_folder_public_albums


class ZoneramaFolder:
    FolderId = str

    gallery: ZoneramaGallery
    id: FolderId

    def __init__(self, gallery: ZoneramaGallery, id: FolderId):
        self.gallery = gallery
        self.id = id

    def get_albums(self) -> list[ZoneramaAlbum]:
        return [
            ZoneramaAlbum(id, self, None)
            for id in get_user_folder_public_albums(self.gallery.username, self.id)
        ]

    @property
    def albums(self) -> list[ZoneramaAlbum]:
        return self.get_albums()
