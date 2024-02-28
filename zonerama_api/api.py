import requests
from bs4 import BeautifulSoup, Tag
import re
import os
from time import sleep
import sys
from collections import namedtuple

from zonerama_api.exceptions import (
    InvalidZoneramaFolderIdException,
    InvalidZoneramaUsernameException,
    InvalidZipIdException,
    UnknownResponseException,
    SecretIdNotSpecifiedException,
)

AlbumId = str
FolderId = str
SecretId = str
Username = str
ZipId = str

ZONERAMA_URL = "https://eu.zonerama.com"

ZIP_REQUEST_URL = "https://zonerama.com/Zip/Album"
ZIP_READY_URL = "https://zonerama.com/Zip/IsReady"
ZIP_SIZE_URL = "https://zonerama.com/Download/Size"
ZIP_DOWNLOAD_URL = "https://zonerama.com/Zip/Download"


def get_user_folder_albums(
    username: Username, folder_id: FolderId, secret_id: SecretId | None = None
) -> list[AlbumId]:
    """Provided with a Zonerama username and a folder id, \
        returns a list of ids of all albums in that folder. \
        The list is sorted as it would appear \
        from top left to bottom right on the web.

    Args:
        username (Username): An existing Zonerama username with a gallery.
        folder_id (FolderId): The id of an existing folder (tab) in the users gallery.
        secret_id (str | None, optional): The secret id. \
            Provide for secret folders, can be found in the URL for them. \
            Defaults to None.

    Raises:
        InvalidZoneramaFolderIdException: \
            The provided folder id is invalid for given username.

    Returns:
        list[AlbumId]: A list of available album's IDs sorted in the aforementioned order.
    """
    response = requests.get(
        f"{ZONERAMA_URL}/{username}/{folder_id}", params={"secret": secret_id}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    slide_div = soup.find(
        attrs={"data-ajax-url": f"/Part/AlbumsInTab?tabId={folder_id}"}
    )

    if slide_div is None:
        raise InvalidZoneramaFolderIdException(folder_id, secret_id)
    assert isinstance(slide_div, Tag)

    mtchs = re.findall(r'data-album-id=\\"([^\\]+)\\"', str(slide_div))
    return mtchs


def get_user_public_folders(username: Username) -> list[FolderId]:
    """Provided with a Zonerama username, \
        returns a list of ids of folders (tabs) in the user's gallery \
        sorted in order which appears as left-to-right on the webpage.

    Args:
        username (Username): An existing Zonerama username with a gallery.

    Raises:
        InvalidZoneramaUsernameException: \
            The provided username is invalid.

    Returns:
        list[FolderId]: A list of public folders in the user's gallery \
        sorted in the aforementioned order.
    """
    response = requests.get(f"{ZONERAMA_URL}/{username}")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    tabs_list_div = soup.find(class_="profile-tabs-list")

    if tabs_list_div is None:
        raise InvalidZoneramaUsernameException(username)
    assert isinstance(tabs_list_div, Tag)

    divs = tabs_list_div.find_all(class_="item")

    return [div["data-tab-id"] for div in divs]


def _get_zip_id(
    album_id: str,
    secret_id: str | None = None,
    include_videos: bool = True,
    original: bool = False,
    av1: bool = False,
    raw: bool = False,
) -> ZipId:
    """Send a request to generate a ZIP file \
        and return the ID of the ZIP file for given album.

    Args:
        album_id (str): The Zonerama album ID
        secret_id (str | None): The secret ID. \
            This is None for non-secret albums.
        include_videos (bool): \
            Whether videos are included or just their thumbnails. \
            Defaults to True.
        original (bool): unknown, defaults to False
        av1 (bool): unknown, defaults to False
        raw (bool): unkonwn, defaults to False

    Returns:
        ZipId: The ID of the requested ZIP file to be used in downloadZip.
    """

    response = requests.get(
        f"{ZIP_REQUEST_URL}/{album_id}",
        {
            "secret": secret_id,
            "includeVideos": include_videos,
            "original": original,
            "av1": av1,
            "raw": raw,
        },
    )
    response.raise_for_status()

    # Does not return a JSON if the album is secret
    # and no secret id was specified. Instead redirects to home page.
    if response.headers["content-type"] != "application/json; charset=utf-8":
        raise SecretIdNotSpecifiedException()

    json = response.json()
    return json["Id"]


def _is_zip_ready(zip_id: ZipId) -> bool:
    response = requests.get(f"{ZIP_READY_URL}/{zip_id}")
    response.raise_for_status()

    if response.headers["content-type"] != "application/json; charset=utf-8":
        raise InvalidZipIdException(zip_id)

    json = response.json()

    if json["Error"] is not None:
        raise InvalidZipIdException(zip_id, json["Error"])

    return json["IsReady"]


def _download_zip(
    zip_id: ZipId, destination_folder: str, sleep_for: float = 5.0
) -> None:
    """Download the generated ZIP file with the provided ID. \
        Note: Downloads an empty archive \
            if downloads are prohibited by the album's author.

    Args:
        zip_id (ZipId): The ID of the generated ZIP file. Output of getZipId.
        destination_folder (str): The destination folder for the ZIP file.
        sleep_for (float, optional): \
            The time for which the function sleeps \
            while the file is not ready, in seconds. Defaults to 5.0.

    Raises:
        InvalidZipIdException: The provided zip_id is invalid.
        UnknownResponseException: The server provided an unkown response.
    """
    response = requests.get(f"{ZIP_DOWNLOAD_URL}/{zip_id}")
    response.raise_for_status()

    if response.headers["content-type"] == "text/html; charset=utf-8":
        match response.text:
            case "ZipID is invalid":
                raise InvalidZipIdException(zip_id)
            # add Zip is not ready

            case _:
                raise UnknownResponseException(response.text)

    assert response.headers["content-type"] == "application/zip"

    content_disposition = response.headers["content-disposition"]
    mtch = re.match(r'attachment; filename="([^"]+)"', content_disposition)
    assert mtch is not None
    filename = mtch.group(1)

    with open(os.path.join(destination_folder, filename), "wb") as df:
        df.write(response.content)


def download_album(
    album_id: AlbumId,
    secret_id: SecretId | None = None,
    include_videos: bool = True,
    original: bool = False,
    av1: bool = False,
    raw: bool = False,
    destination_folder: str = os.getcwd(),
    sleep_for: float = 5.0,
) -> None:
    """Downloads the Zonerama album with the provided ID as a ZIP file. \
        If the album is a secret one, secret_id must be specified. \
        If the author has prohibited downloads, downloads an empty archive.

    Args:
        album_id (AlbumId): The ID of the album you wish to download. \
            This is the string of numbers, \
            which can be found in the URL after Album/.
        secret_id (SecretId | None, optional): The secret id. \
            Provide for secret albums, can be found in the URL for them. \
            Defaults to None.
        include_videos (bool, optional): Whether videos are included \
            or just their thumbnails. Defaults to True.
        original (bool): unknown, defaults to False
        av1 (bool): unknown, defaults to False
        raw (bool): unkonwn, defaults to False
        destination_folder (str, optional): \
            The destination folder for the ZIP file. Defaults to os.getcwd().
        sleep_for (float, optional): The time for which the function sleeps \
            while the file is not ready, in seconds. Defaults to 5.0.
    """
    zip_id = _get_zip_id(album_id, secret_id, include_videos, original, av1, raw)

    while not _is_zip_ready(zip_id):
        print(f"Waiting on zip_id: {zip_id}, {sleep_for}s", file=sys.stderr)
        sleep(sleep_for)

    _download_zip(zip_id, destination_folder, sleep_for)


class AlbumSize:
    photo_count: int
    video_count: int
    zip_size: float # in bytes

    def __init__(self, photo_count: int, video_count: int, zip_size: float) -> None:
        self.photo_count = photo_count
        self.video_count = video_count
        self.zip_size = zip_size


def get_album_size(
    album_id: AlbumId, videos: bool = True, secret_id: SecretId | None = None
) -> AlbumSize:
    response = requests.post(
        ZIP_SIZE_URL,
        data={
            "albumId": album_id,
            "photoId": "",
            "filter": "",
            "secret": secret_id,
            "download_Album": False,
            "download_Videos": videos,
            "download_RAWs": False,
        },
    )

    if response.headers["content-type"] != "application/json; charset=utf-8":
        raise SecretIdNotSpecifiedException()

    txt = response.json()["text"]
    mtch = re.match(
        r"Předpokládaná velikost archivu (?P<photo_count>\d+) fotek"
        r"(?: a (?P<video_count>\d+) videí)?"
        r" je (?P<size_whole>\d+),(?P<size_dec>\d+) (?P<unit>[kMG]B).",
        txt,
    )
    assert mtch is not None

    video_count = "0" if mtch["video_count"] is None else mtch["video_count"]
    size_num = float(f"{mtch['size_whole']}.{mtch['size_dec']}")

    def into_bytes(num: float, unit: str) -> float:
        match unit:
            case "kB":
                return num * 1_024
            case "MB":
                return num * (1_024 ** 2)
            case "GB":
                return num * (1_024 ** 3)
            case _:
                assert False

    return AlbumSize(
        int(mtch["photo_count"]),
        int(video_count),
        into_bytes(size_num, mtch["unit"]),
    )
