from zonerama_downloader.zonerama_folder import ZoneramaFolder
from zonerama_downloader.zonerama_album import ZoneramaAlbum
from zonerama_downloader.zonerama_api import get_user_public_folders


class ZoneramaGallery:
    Username = str

    username: Username

    def __init__(self, username: Username):
        self.username = username

    def get_public_folders(self) -> list[ZoneramaFolder]:
        return get_user_public_folders(self)

    @property
    def public_folders(self) -> list[ZoneramaFolder]:
        return self.get_public_folders()

    def get_public_albums(self) -> list[ZoneramaAlbum]:
        result: list[ZoneramaAlbum] = []
        for folder in self.public_folders:
            result += folder.albums
        return result

    @property
    def public_albums(self) -> list[ZoneramaAlbum]:
        return self.get_public_albums()
