from zonerama_downloader.zonerama_folder import ZoneramaFolder

class ZoneramaGallery:
    Username = str

    username: Username

    def __init__(self, username: Username):
        self.username = username

    def get_folders(self) -> list[ZoneramaFolder]:
        pass
