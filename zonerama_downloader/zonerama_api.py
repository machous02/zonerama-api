import requests
from bs4 import BeautifulSoup, Tag
import re

from exceptions import InvalidZoneramaFolderIdException, InvalidZoneramaUsernameException

AlbumId = str
FolderId = str
Username = str

ZONERAMA_URL = "https://eu.zonerama.com"


def get_user_folder_public_albums(
    username: Username, folder_id: FolderId
) -> list[AlbumId]:
    """Provided with a Zonerama username and a folder id, \
        returns a list of ids of all albums in that folder.

    Args:
        username (Username): An existing Zonerama username with a gallery.
        folder_id (FolderId): The id of an existing folder (tab) in the users gallery.

    Raises:
        InvalidZoneramaFolderIdException: \
            The provided folder id is invalid for given username.

    Returns:
        list[AlbumId]: A list of available album's IDs.
    """
    response = requests.get(f"{ZONERAMA_URL}/{username}/{folder_id}")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    slide_div = soup.find(
        attrs={"data-ajax-url": f"/Part/AlbumsInTab?tabId={folder_id}"}
    )

    if slide_div is None:
        raise InvalidZoneramaFolderIdException(folder_id)
    assert isinstance(slide_div, Tag)

    mtchs = re.findall(r'data-album-id=\\"([^\\]+)\\"', str(slide_div))
    return mtchs


def get_user_public_folders(username: Username) -> list[FolderId]:
    """Provided with a Zonerama username, \
        returns a list of ids of folders (tabs) in the user's gallery.

    Args:
        username (Username): An existing Zonerama username with a gallery.

    Raises:
        InvalidZoneramaUsernameException: \
            The provided username is invalid.

    Returns:
        list[FolderId]: A list of public folders in the user's gallery.
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
