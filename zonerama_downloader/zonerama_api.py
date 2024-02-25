import requests
from bs4 import BeautifulSoup, Tag


album_id_t = str
folder_id_t = str
username_t = str

ZONERAMA_URL = 'https://eu.zonerama.com'


# def getFolderAlbums(username: username_t, folder_id: folder_id_t) -> list[album_id_t]:
#     # response = requests.get(f'{ZONERAMA_URL}/{username}/{folder_id}')
#     response = requests.get('https://eu.zonerama.com/mustangove/1302305')
#     response.raise_for_status()

#     print(response.text)

#     tree = html.parse(StringIO(response.text))
#     selector = CSSSelector('.list-alb')
#     for i in selector(tree):
#         print(i)

def get_user_public_folders(username: username_t) -> list[folder_id_t]:
    response = requests.get(f'{ZONERAMA_URL}/{username}')
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'lxml')
    tabs_list_div = soup.find(class_='profile-tabs-list')
    assert isinstance(tabs_list_div, Tag)

    divs = tabs_list_div.find_all(class_='item')

    return [div['data-tab-id'] for div in divs]
