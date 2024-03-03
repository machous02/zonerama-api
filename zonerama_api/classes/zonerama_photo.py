from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zonerama_api.classes.zonerama_album import ZoneramaAlbum

from zonerama_api.typing import PhotoId

class ZoneramaPhoto:
    id: PhotoId
    album: ZoneramaAlbum