from datetime import datetime
from typing import Any, TypeAlias

def map_attributes(mapping: dict[str, str]):
    def decorator(cls: Any):
        original_init = cls.__init__

        def init_wrapper(self: Any, obj: Any, *args: tuple[Any], **kwargs: dict[str, Any]):
            for class_attr, obj_key in mapping.items():
                setattr(self, class_attr, getattr(obj, obj_key))
            original_init(self, *args, **kwargs)

        cls.__init__ = init_wrapper
        return cls

    return decorator


@map_attributes(
    {
        "success": "Success",
        "message": "Message",
        "code": "Code",
        "result": "Result",
    }
)
class ApiResponse:
    success: bool
    message: str | None
    code: str | None
    result: object


AccountID: TypeAlias = int


@map_attributes(
    {
        "id": "ID",
        "zaid": "ZAID",
        "email": "EMail",
        "name": "Name",
        "domain": "Domain",
        "full_name": "FullName",
        "language": "Language",
        "country": "Country",
        "text": "Text",
        "inserted": "Inserted",
        "last_access": "LastAccess",
        "changed": "Changed",
        "change_avatar": "ChangeAvatar",
        "page_url": "PageUrl",
        "avatar_url": "AvatarUrl",
        "profile_photo_url": "ProfilePhotoUrl",
        "max_albums": "MaxAlbums",
        "max_photos": "MaxPhotos",
        "max_size": "MaxSize",
        "albums": "Albums",
        "photos": "Photos",
        "size": "Size",
        "likes": "Likes",
    }
)
class AccountInfo:
    id: AccountID
    zaid: int
    email: str | None
    name: str | None
    domain: str | None
    full_name: str | None
    language: str | None
    country: str | None
    text: str | None
    inserted: datetime
    last_access: datetime | None
    changed: datetime | None
    change_avatar: datetime | None
    page_url: str | None
    avatar_url: str | None
    profile_photo_url: str | None
    max_albums: int
    max_photos: int
    max_size: int
    albums: int
    photos: int
    size: int
    likes: int


TabID: TypeAlias = int


@map_attributes(
    {
        "id": "ID",
        "account_id": "AccountID",
        "name": "Name",
        "rank": "Rank",
        "secret": "Secret",
        "password": "Pwd",
        "password_help": "PwdHelp",
    }
)
class TabInfo:
    id: TabID
    account_id: AccountID
    name: str | None
    rank: int
    secret: str
    password: str
    password_help: str
