import os
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

from zonerama_api.exceptions import InvalidPhotoIdException
from zonerama_api.typing import PhotoId

PHOTO_DOWNLOAD_URL = "https://zonerama.com/Download/Photo"
PHOTO_INFO_URL = "https://eu.zonerama.com/Part/PhotoOnSlide"


def download_photo(photo_id: PhotoId, destination_folder: str = os.getcwd()) -> None:
    response = requests.get(f"{PHOTO_DOWNLOAD_URL}/{photo_id}")
    response.raise_for_status()

    if response.headers["content-type"] == "text/html; charset=utf-8":
        raise InvalidPhotoIdException(photo_id)

    assert response.headers["content-type"].startswith(("image", "video"))

    content_disposition = response.headers["content-disposition"]
    mtch = re.match(r'attachment; filename="?([^"]+)"?', content_disposition)
    assert mtch is not None
    filename = mtch.group(1)

    with open(os.path.join(destination_folder, filename), "wb") as df:
        df.write(response.content)


@dataclass
class PhotoInfo:
    name: str
    size: str
    resolution: tuple[int, int, int]
    date_added: str
    author: str
    copyright: str
    created_date: str
    changed_date: str
    iso: int
    exposure_time: str
    aperature: float
    focal_length: str
    effective_focal_length: str
    lens: str
    exposure_compensation: str
    color_profile: str
    camera: str
    software: str


def get_photo_info(photo_id: PhotoId) -> PhotoInfo:  # WIP
    pass

    response = requests.get(PHOTO_INFO_URL, params={"ID": photo_id})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features="lxml")
    param = soup.find("div", class_="param")
    assert isinstance(param, Tag)
    tbody = param.find("tbody")
    assert isinstance(tbody, Tag)

    params = [
        tr.find_all("td")[1].text.strip() for tr in tbody.find_all("tr") if len(tr) >= 2
    ]
    return PhotoInfo(*params)
