import requests
import os
import re
from time import sleep
import sys

from zonerama_downloader.exceptions import (
    InvalidZipIdException,
    UnknownResponseException,
    SecretIdNotSpecifiedException,
)


ZIP_REQUEST_URL = "https://zonerama.com/Zip/Album"
ZIP_READY_URL = "https://zonerama.com/Zip/IsReady"
ZIP_DOWNLOAD_URL = "https://zonerama.com/Zip/Download"


def _get_zip_id(
    album_id: str,
    secret_id: str | None = None,
    include_videos: bool = True,
    original: bool = False,
    av1: bool = False,
    raw: bool = False,
) -> str:
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
        str: The ID of the requested ZIP file to be used in downloadZip.
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


def _is_zip_ready(zip_id: str) -> bool:
    response = requests.get(f"{ZIP_READY_URL}/{zip_id}")
    response.raise_for_status()

    if response.headers["content-type"] != "application/json; charset=utf-8":
        raise InvalidZipIdException(zip_id)

    json = response.json()

    if json["Error"] is not None:
        raise InvalidZipIdException(zip_id, json["Error"])

    return json["IsReady"]


def _download_zip(zip_id: str, destination_folder: str, sleep_for: float = 5.0) -> None:
    """Download the generated ZIP file with the provided ID. \
        Wait while the file is not ready.
        Note: Downloads an empty archive \
            if downloads are prohibited by the album's author.

    Args:
        zip_id (str): The ID of the generated ZIP file. Output of getZipId.
        destination_folder (str): The destination folder for the ZIP file.
        sleep_for (float, optional): \
            The time for which the function sleeps \
            while the file is not ready, in seconds. Defaults to 5.0.

    Raises:
        InvalidZipIdException: The provided zip_id is invalid.
        UnknownResponseException: The server provided an unkown response.
    """
    while not _is_zip_ready(zip_id):
        print(f'Waiting on zip_id: {zip_id}, {sleep_for}s', file=sys.stderr)
        sleep(sleep_for)

    response = requests.get(f"{ZIP_DOWNLOAD_URL}/{zip_id}")
    response.raise_for_status()

    if response.headers["content-type"] == "text/html; charset=utf-8":
        match response.text:
            case "ZipID is invalid":
                raise InvalidZipIdException(zip_id)

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
    album_id: str,
    secret_id: str | None = None,
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
        album_id (str): The ID of the album you wish to download. \
            This is the string of numbers, \
            which can be found in the URL after Album/.
        secret_id (str | None, optional): The secret id. \
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
    _download_zip(zip_id, destination_folder, sleep_for)
