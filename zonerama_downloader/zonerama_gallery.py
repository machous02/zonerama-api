from zonerama_downloader.zonerama_folder import ZoneramaFolder
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
