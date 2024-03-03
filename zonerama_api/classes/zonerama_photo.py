from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_api.classes.zonerama_album import ZoneramaAlbum

from zonerama_api.z_typing import PhotoId
from zonerama_api.api import download_photo

class ZoneramaPhoto:
    id: PhotoId
    album: ZoneramaAlbum

    def __init__(self, id: PhotoId, album: ZoneramaAlbum) -> None:
        self.id = id
        self.album = album

    def download(self, destination_folder: str) -> None:
        download_photo(self.id, destination_folder)