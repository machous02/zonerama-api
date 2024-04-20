from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

from zonerama_api.exceptions import InvalidZoneramaUsernameException
from zonerama_api.typing import FolderId, UserId, Username

ZONERAMA_URL = "https://eu.zonerama.com"
PROFILE_BASE_URL = "https://eu.zonerama.com/Profile"


@dataclass
class GalleryInfo:
    name: str
    description: str


def get_gallery_info(username: Username) -> GalleryInfo:
    response = requests.get(
        f"{ZONERAMA_URL}/{username}",
        allow_redirects=False,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features="lxml")
    meta = soup.find_all("meta")

    assert all(map(lambda x: isinstance(x, Tag), meta))

    meta_dict: dict[str, str] = {}
    for tag in meta:
        key, value = tag["property"], tag["content"]
        assert isinstance(key, str) and isinstance(value, str)

        meta_dict[key] = value

    return GalleryInfo(
        name=meta_dict["og:title"], description=meta_dict["og:description"]
    )


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


def is_user_id(identificator: str) -> bool:
    return identificator.isdigit()


def get_username(user_id: UserId) -> Username:
    response = requests.get(f"{PROFILE_BASE_URL}/{user_id}")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features="lxml")
    account_tag = soup.find("meta", property="og:title")
    assert isinstance(account_tag, Tag)

    username = account_tag["content"]
    assert isinstance(username, str)
    return username
