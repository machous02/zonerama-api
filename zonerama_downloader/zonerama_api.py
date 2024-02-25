import requests
from bs4 import BeautifulSoup, Tag
import re

album_id_t = str
folder_id_t = str
username_t = str

ZONERAMA_URL = "https://eu.zonerama.com"


def get_user_folder_public_albums(
    username: username_t, folder_id: folder_id_t
) -> list[album_id_t]:
    response = requests.get(f"{ZONERAMA_URL}/{username}/{folder_id}")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    slide_div = soup.find(
        attrs={"data-ajax-url": f"/Part/AlbumsInTab?tabId={folder_id}"}
    )
    assert isinstance(slide_div, Tag)

    mtchs = re.findall(r'data-album-id=\\"([^\\]+)\\"', str(slide_div))
    return mtchs


def get_user_public_folders(username: username_t) -> list[folder_id_t]:
    response = requests.get(f"{ZONERAMA_URL}/{username}")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    tabs_list_div = soup.find(class_="profile-tabs-list")
    assert isinstance(tabs_list_div, Tag)

    divs = tabs_list_div.find_all(class_="item")

    return [div["data-tab-id"] for div in divs]
