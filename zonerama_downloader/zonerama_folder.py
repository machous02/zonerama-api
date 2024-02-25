from zonerama_downloader.zonerama_gallery import ZoneramaGallery
from zonerama_downloader.zonerama_album import ZoneramaAlbum
from zonerama_downloader.zonerama_api import get_public_folder_albums


class ZoneramaFolder:
    FolderId = str

    gallery: ZoneramaGallery
    id: FolderId

    def __init__(self, gallery: ZoneramaGallery, id: FolderId):
        self.gallery = gallery
        self.id = id

    def get_albums(self) -> list[ZoneramaAlbum]:
        return get_public_folder_albums(self)

    @property
    def albums(self) -> list[ZoneramaAlbum]:
        return self.get_albums()
