from zonerama_api.classes.zonerama_gallery import ZoneramaGallery
from zonerama_api.api import get_username

zg = ZoneramaGallery('Renda7')

for folder in zg.get_public_folders():
    for album in folder.albums:
        print(album.name)
