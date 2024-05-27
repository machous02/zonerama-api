from datetime import datetime
from typing import Any, TypeAlias

import zonerama_api.android.android_exceptions as zaexc


def map_attributes(mapping: dict[str, str]):
    def decorator(cls: Any):
        original_init = cls.__init__

        def init_wrapper(
            self: Any, obj: Any, *args: tuple[Any], **kwargs: dict[str, Any]
        ):
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

    def raise_for_code(self) -> None:
        if self.code is None:
            return

        match self.code:
            case "E_ZONERAMA_INVALIDPARAMS":
                raise zaexc.ZoneramaAndroidInvalidLoginException(
                    self.code, self.message
                )
            case "E_ZONERAMA_UNKNOWNACCOUNTID":
                raise zaexc.ZoneramaAndroidUnknownAccountID(self.code, self.message)
            case "E_ZONERAMA_LOGINFAILED":
                raise zaexc.ZoneramaAndroidWrongPasswordException(
                    self.code, self.message
                )
            case "E_ZONERAMA_NEEDLOGIN":
                raise zaexc.ZoneramaAndroidNotLoggedInException(self.code, self.message)
            case "E_ZONERAMA_UNKNOWNACCOUNTID":
                raise zaexc.ZoneramaAndroidUnknownAccountID(self.code, self.message)
            case "E_ZONERAMA_ACCESSDENIED":
                raise zaexc.ZoneramaAndroidAccessDenied(self.code, self.message)
            case "E_ZONERAMA_UNKNOWNTABID":
                raise zaexc.ZoneramaAndroidUnknownTabID(self.code, self.message)
            case "E_ZONERAMA_UNKNOWNALBUMID":
                raise zaexc.ZoneramaAndroidUnknownAlbumID(self.code, self.message)
            case _:
                print(self.code)
                assert False


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
        "is_password_protected": "IsPasswordProtected",
        "public": "Public",
        "changed": "Changed",
        "type": "Type",
        "page_url": "PageUrl",
    }
)
class TabInfo:
    id: TabID
    account_id: AccountID
    name: str | None
    rank: int
    secret: str | None
    password: str | None
    password_help: str | None
    is_password_protected: bool
    public: bool
    changed: datetime | None
    type: str
    page_url: str | None


AlbumID: TypeAlias = int
PhotoID: TypeAlias = int


@map_attributes(
    {
        "id": "ID",
        "parent_id": "ParentID",
        "account_id": "AccountID",
        "photo_id": "PhotoID",
        "name": "Name",
        "inserted": "Inserted",
        "changed": "Changed",
        "updated": "Updated",
        "text": "Text",
        "password": "Pwd",
        "password_help": "PwdHelp",
        "secret": "Secret",
        "public_list": "PublicList",
        "path_of_id": "PathOfID",
        "path_of_name": "PathOfName",
        "path_level": "PathLevel",
        "protected": "Protected",
        "longitude": "Longitude",
        "latitude": "Latitude",
        "tab_id": "TabID",
        "facebook_synced": "FacebookSynced",
        "page_url": "PageUrl",
        "image_url": "ImageUrl",
        "image_pattern_url": "ImagePatternUrl",
        "is_password_protected": "IsPasswordProtected",
        "is_private": "IsPrivate",
        "is_protected": "IsProtected",
        "is_public": "IsPublic",
        "is_secret": "IsSecret",
        "type": "Type",
        "albums": "Albums",
        "photos": "Photos",
        "size": "Size",
        "comments": "Comments",
        "browse": "Browse",
        "like": "Like",
    }
)
class AlbumInfo:
    id: AlbumID
    parent_id: int | None
    account_id: AccountID
    photo_id: PhotoID | None
    name: str | None
    inserted: datetime
    changed: datetime | None
    updated: datetime | None
    text: str | None
    password: str | None
    password_help: str | None
    secret: str | None
    public_list: bool
    path_of_id: str | None
    path_of_name: str | None
    path_level: int
    protected: str | None
    longitude: float | None
    latitude: float | None
    tab_id: TabID
    facebook_synced: int
    page_url: str | None
    image_url: str | None
    image_pattern_url: str | None
    is_password_protected: bool
    is_private: bool
    is_protected: bool
    is_public: bool
    is_secret: bool
    type: str
    albums: int
    photos: int
    size: int
    comments: int
    browse: int
    like: int
