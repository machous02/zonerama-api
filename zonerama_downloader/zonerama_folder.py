from zonerama_downloader.zonerama_gallery import ZoneramaGallery
from zonerama_downloader.zonerama_album import ZoneramaAlbum


class ZoneramaFolder:
    FolderId = str

    gallery: ZoneramaGallery
    id: FolderId

    def __init__(self, gallery: ZoneramaGallery, id: FolderId):
        self.gallery = gallery
        self.id = id

    def get_albums(self) -> list[ZoneramaAlbum]:
        pass
