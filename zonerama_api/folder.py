import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

from zonerama_api.exceptions import (
    InvalidZoneramaFolderIdException,
    InvalidZoneramaFolderPasswordException,
    InvalidZoneramaUsernameException,
    SecretIdNotSpecifiedException,
    ZoneramaFolderLockedException,
)
from zonerama_api.typing import AlbumId, FolderId, FolderPassword, SecretId, Username

ZONERAMA_URL = "https://eu.zonerama.com"
FOLDER_ALBUMS_URL = "https://eu.zonerama.com/Part/AlbumsInTab"
FOLDER_UNLOCK_URL = "https://eu.zonerama.com/Web/UnlockTab"


@dataclass
class FolderInfo:
    name: str


def get_folder_info(username: Username, folder_id: FolderId) -> FolderInfo:
    response = requests.get(f"{ZONERAMA_URL}/{username}")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    tabs_list_div = soup.find(class_="profile-tabs-list")

    if tabs_list_div is None:
        raise InvalidZoneramaUsernameException(username)
    assert isinstance(tabs_list_div, Tag)

    div = tabs_list_div.find("div", attrs={"data-tab-id": folder_id})
    assert isinstance(div, Tag)
    name = div.find("span", class_="name")
    assert isinstance(name, Tag)

    return FolderInfo(name=name.text)


def folder_exists(
    folder_id: FolderId,
) -> bool:
    response = requests.get(
        FOLDER_ALBUMS_URL, params={"tabId": folder_id}, allow_redirects=False
    )
    # non-existent
    if response.status_code == 404:
        return False

    # deleted
    if response.status_code == 500:
        return False

    response.raise_for_status()

    # secret
    if response.status_code == 302:
        return True

    return True


def is_folder_locked(
    folder_id: FolderId,
    secret_id: SecretId | None = None,
) -> bool:
    response = requests.get(
        FOLDER_ALBUMS_URL,
        params={"tabId": folder_id, "secret": secret_id},
        allow_redirects=False,
    )
    response.raise_for_status()

    if response.status_code == 302:
        raise SecretIdNotSpecifiedException()

    soup = BeautifulSoup(response.text, "lxml")
    lock_i = soup.find(class_="icon-lock")
    return lock_i is not None


def unlock_folder(
    folder_id: FolderId, password: FolderPassword, session: requests.Session
) -> bool:
    response = session.post(
        url=FOLDER_UNLOCK_URL, data={"value": password}, params={"ID": folder_id}
    )
    response.raise_for_status()

    return response.json()["Success"]


def get_folder_albums(
    folder_id: FolderId,
    secret_id: SecretId | None = None,
    password: FolderPassword | None = None,
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
    if not folder_exists(folder_id):
        raise InvalidZoneramaFolderIdException(folder_id)

    session = requests.Session()

    if is_folder_locked(folder_id, secret_id):
        if password is None:
            raise ZoneramaFolderLockedException(folder_id, secret_id)

        if not unlock_folder(folder_id, password, session):
            raise InvalidZoneramaFolderPasswordException(folder_id, password)

    response = session.get(
        FOLDER_ALBUMS_URL,
        params={"tabId": folder_id, "secret": secret_id},
        allow_redirects=False,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    script = soup.find("script")
    assert script is not None
    assert isinstance(script, Tag)

    mtchs = re.findall(r'data-album-id=\\"([^\\]+)\\"', str(script))
    return mtchs
