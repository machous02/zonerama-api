from zonerama_api.classes.zonerama_gallery import ZoneramaGallery

zg = ZoneramaGallery('Renda7')

for folder in zg.get_public_folders():
    for album in folder.albums:
        print(album.name)