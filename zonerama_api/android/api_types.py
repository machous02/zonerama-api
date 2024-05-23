from dataclasses import dataclass
from typing import Any
from datetime import datetime

@dataclass
class base64Binary:
    pass

@dataclass
class SimpleResultOfObject:
    Success: bool
    Message: str | None
    Code: str | None
    Result: Any | None


@dataclass
class SimpleResult(SimpleResultOfObject):
    pass


@dataclass
class LoginAndroid:
    email: str | None
    pwd: str | None
    culture: str | None
    version: float
    data1: str | None
    data2: str | None


@dataclass
class LoginAndroidResponse:
    LoginAndroidResult: SimpleResult | None


@dataclass
class Id_Name:
    ID: int
    Name: str | None


@dataclass
class ArrayOfId_Name:
    Id_Name_: list[Id_Name] | None


@dataclass
class CreateAlbumAndroid:
    name: str | None
    text: str | None
    level: int
    pwd: str | None


@dataclass
class CreateAlbumAndroidResponse:
    CreateAlbumAndroidResult: SimpleResult | None


@dataclass
class CreateAlbumInTabAndroid:
    tabId: int
    name: str | None
    text: str | None
    pwd: str | None


@dataclass
class CreateAlbumInTabAndroidResponse:
    CreateAlbumInTabAndroidResult: SimpleResult | None


@dataclass
class CreateAccount:
    email: str | None


@dataclass
class CreateAccountResponse:
    CreateAccountResult: SimpleResult | None


@dataclass
class ResetPwd:
    email: str | None


@dataclass
class ResetPwdResponse:
    ResetPwdResult: SimpleResult | None


@dataclass
class TestResult:
    success: bool
    result: int
    message: str | None
    code: str | None


@dataclass
class TestResultResponse:
    TestResultResult: SimpleResult | None


@dataclass
class CheckPermissions:
    service: str | None
    permissions: str | None


@dataclass
class CheckPermissionsResponse:
    CheckPermissionsResult: SimpleResult | None


@dataclass
class IsAuthorized:
    pass


@dataclass
class SimpleResultOfBoolean:
    Success: bool
    Message: str | None
    Code: str | None
    Result: bool


@dataclass
class IsAuthorizedResponse:
    IsAuthorizedResult: SimpleResultOfBoolean | None


@dataclass
class GetVersion:
    pass


@dataclass
class Version:
    Current: float
    CompatibleMinimum: float


@dataclass
class SimpleResultOfVersion:
    Success: bool
    Message: str | None
    Code: str | None
    Result: Version | None


@dataclass
class GetVersionResponse:
    GetVersionResult: SimpleResultOfVersion | None


@dataclass
class ArrayOfInt:
    int_: list[int] | None


@dataclass
class CreateAlbum:
    parentAlbumID: int | None
    name: str | None
    text: str | None
    categories: ArrayOfInt | None
    public: bool | None


@dataclass
class CreateAlbumResponse:
    CreateAlbumResult: SimpleResult | None


@dataclass
class CreateIsolatedAlbum:
    name: str | None
    expire: datetime | None


@dataclass
class CreateIsolatedAlbumResponse:
    CreateIsolatedAlbumResult: SimpleResult | None


@dataclass
class UpdateAlbumSecurity:
    albumID: int
    recursive: int
    level: int
    publicList: bool | None
    pwd: str | None


@dataclass
class UpdateAlbumSecurityResponse:
    UpdateAlbumSecurityResult: SimpleResult | None


@dataclass
class UpdateAlbumPwd:
    albumID: int
    pwd: str | None
    pwdHelp: str | None


@dataclass
class UpdateAlbumPwdResponse:
    UpdateAlbumPwdResult: SimpleResult | None


@dataclass
class UpdateAlbum:
    albumID: int
    name: str | None
    text: str | None
    categories: ArrayOfInt | None
    defaultOrder: str | None


@dataclass
class UpdateAlbumResponse:
    UpdateAlbumResult: SimpleResult | None


@dataclass
class UpdateAlbumCover:
    albumID: int
    photoID: int | None


@dataclass
class UpdateAlbumCoverResponse:
    UpdateAlbumCoverResult: SimpleResult | None


@dataclass
class UpdateAlbumPhotosRank:
    albumID: int
    sorted: ArrayOfInt | None


@dataclass
class UpdateAlbumPhotosRankResponse:
    UpdateAlbumPhotosRankResult: SimpleResult | None


@dataclass
class UpdateAlbumsRank:
    sorted: ArrayOfInt | None


@dataclass
class UpdateAlbumsRankResponse:
    UpdateAlbumsRankResult: SimpleResult | None


@dataclass
class UpdateTabsRank:
    sorted: ArrayOfInt | None


@dataclass
class UpdateTabsRankResponse:
    UpdateTabsRankResult: SimpleResult | None


@dataclass
class DeleteAlbum:
    albumID: int


@dataclass
class DeleteAlbumResponse:
    DeleteAlbumResult: SimpleResult | None


@dataclass
class DeleteAlbums:
    albumID: ArrayOfInt | None


@dataclass
class DeleteAlbumsResponse:
    DeleteAlbumsResult: SimpleResult | None


@dataclass
class UnlockAlbum:
    albumID: int
    pwd: str | None


@dataclass
class UnlockAlbumResponse:
    UnlockAlbumResult: SimpleResult | None


@dataclass
class UpdateAlbumFacebook:
    albumID: int
    sync: int | None
    deleteFbAlbum: bool | None


@dataclass
class UpdateAlbumFacebookResponse:
    UpdateAlbumFacebookResult: SimpleResult | None


@dataclass
class CreatePhoto:
    albumID: int
    name: str | None
    text: str | None
    stream: base64Binary | None


@dataclass
class CreatePhotoResponse:
    CreatePhotoResult: SimpleResult | None


@dataclass
class UpdatePhotoExif:
    photoID: int
    name: str | None
    created: datetime | None
    camHwMaker: str | None
    camHwModel: str | None
    focalLength: str | None
    focalLength35: str | None
    focalRange: str | None
    flash: str | None
    iso: str | None
    exposureTime: str | None
    aperture: str | None
    keywords: str | None
    author: str | None


@dataclass
class UpdatePhotoExifResponse:
    UpdatePhotoExifResult: SimpleResult | None


@dataclass
class UpdatePhotoStream:
    photoID: int
    stream: base64Binary | None


@dataclass
class UpdatePhotoStreamResponse:
    UpdatePhotoStreamResult: SimpleResult | None


@dataclass
class UpdatePhoto:
    photoID: int
    name: str | None
    text: str | None


@dataclass
class UpdatePhotoResponse:
    UpdatePhotoResult: SimpleResult | None


@dataclass
class UpdatePhotoLocation:
    photoID: int
    lat: float | None
    lng: float


@dataclass
class UpdatePhotoSecurity:
    photoID: int
    level: int
    publicList: bool | None
    pwd: str | None
    resetSecret: bool


@dataclass
class UpdatePhotoSecurityResponse:
    UpdatePhotoSecurityResult: SimpleResult | None


@dataclass
class UpdatePhotoRotateFlip:
    photoID: int
    rotate: int


@dataclass
class UpdatePhotoRotateFlipResponse:
    UpdatePhotoRotateFlipResult: SimpleResult | None


@dataclass
class UpdatePhotoLicence:
    photoID: int
    cc: bool | None
    enableDownload: bool | None
    enableCommercial: bool | None
    enableModification: bool | None


@dataclass
class UpdatePhotoLicenceResponse:
    UpdatePhotoLicenceResult: SimpleResult | None


@dataclass
class UnlockPhoto:
    photoID: int
    pwd: str | None


@dataclass
class UnlockPhotoResponse:
    UnlockPhotoResult: SimpleResult | None


@dataclass
class DeletePhoto:
    photoID: int


@dataclass
class DeletePhotoResponse:
    DeletePhotoResult: SimpleResult | None


@dataclass
class DeletePhotoFromMobileDevices:
    photoID: int


@dataclass
class DeletePhotoFromMobileDevicesResponse:
    DeletePhotoFromMobileDevicesResult: SimpleResult | None


@dataclass
class DeletePhotos:
    photoID: ArrayOfInt | None


@dataclass
class DeletePhotosResponse:
    DeletePhotosResult: SimpleResult | None


@dataclass
class MovePhotos:
    photoId: ArrayOfInt | None
    albumId: int


@dataclass
class MovePhotosResponse:
    MovePhotosResult: SimpleResult | None


@dataclass
class CopyPhotos:
    photId: ArrayOfInt | None
    albumId: int


@dataclass
class CopyPhotosResponse:
    CopyPhotosResult: SimpleResult | None


@dataclass
class CreateComment:
    joinID: int
    joinTable: int
    text: str | None


@dataclass
class CreateCommentResponse:
    CreateCommentResult: SimpleResult | None


@dataclass
class UpdateComment:
    commentID: int
    text: str | None


@dataclass
class UpdateCommentResponse:
    UpdateCommentResult: SimpleResult | None


@dataclass
class DeleteComment:
    commentID: int


@dataclass
class DeleteCommentResponse:
    DeleteCommentResult: SimpleResult | None


@dataclass
class UpdateVideoCover:
    photoID: int
    thumbnailName: str | None


@dataclass
class UpdateVideoCoverResponse:
    UpdateVideoCoverResult: SimpleResult | None


@dataclass
class UpdateAvatar:
    stream: base64Binary | None


@dataclass
class UpdateAvatarResponse:
    UpdateAvatarResult: SimpleResult


@dataclass
class DeleteAvatar:
    pass


@dataclass
class DeleteAvatarResponse:
    DeleteAvatarResult: SimpleResult | None


@dataclass
class ExistsAvatar:
    pass


@dataclass
class ExistsAvatarResponse:
    ExistsAvatarResult: bool


@dataclass
class Login:
    email: str | None
    pwd: str | None


@dataclass
class LoginResponse:
    LoginResult: SimpleResult | None


@dataclass
class LoginByGuid:
    guid: str | None


@dataclass
class LoginByGuidResponse:
    LoginByGuidResult: SimpleResult | None


@dataclass
class LoginByAuthKey:
    key: str | None


@dataclass
class LoginByAuthKeyResponse:
    LoginByAuthKeyResult: SimpleResult | None


@dataclass
class LoginZA:
    email: str | None
    pwd: str | None


@dataclass
class LoginZAResponse:
    LoginZAResult: SimpleResult | None


@dataclass
class SaveLogin:
    pass


@dataclass
class SaveLoginResponse:
    SaveLoginResult: SimpleResult | None


@dataclass
class Logout:
    pass


@dataclass
class LogoutResponse:
    LogoutResult: SimpleResult | None


@dataclass
class DeleteAccount:
    pass


@dataclass
class DeleteAccountResponse:
    DeleteAccountResult: SimpleResult | None


@dataclass
class UpdateAccountSettings:
    seo: bool | None
    news: bool | None
    newsOnDashboard: bool | None


@dataclass
class UpdateAccountSettingsResponse:
    UpdateAccountSettingsResult: SimpleResult | None


@dataclass
class Like:
    id: int
    table: int


@dataclass
class LikeResponse:
    LikeResult: SimpleResult | None


@dataclass
class Unlike:
    id: int
    table: int


@dataclass
class UnlikeResponse:
    UnlikeResult: SimpleResult | None


@dataclass
class ArrayOfString:
    string: list[str] | None


@dataclass
class PhotoSettings:
    MaxResolution: str | None
    MinResolution: str | None
    MaxSize: int
    JpegQuality: int
    SupportedFiles: ArrayOfString | None


@dataclass
class SimpleResultOfPhotoSettings:
    Success: bool
    Message: str | None
    Code: str | None
    Result: PhotoSettings | None


@dataclass
class GetPhotoSettings:
    pass


@dataclass
class GetPhotoSettingsResponse:
    GetPhotoSettingsResult: SimpleResultOfPhotoSettings | None


@dataclass
class CreateTab:
    name: str | None
    public: bool
    rank: int | None
    pwd: str | None
    pwdHelp: str | None


@dataclass
class CreateTabResponse:
    CreateTabResult: SimpleResult | None


@dataclass
class DeleteTab:
    id: int


@dataclass
class DeleteTabResponse:
    DeleteTabResult: SimpleResult | None


@dataclass
class UpdateTab:
    id: int
    name: str | None
    public: bool | None
    rank: int | None
    pwd: str | None
    pwdHelp: str | None
    defaultOrder: str | None


@dataclass
class UpdateTabResponse:
    UpdateTabResult: SimpleResult | None


@dataclass
class UpdateAlbumsTab:
    albumId: ArrayOfInt | None
    tabId: int


@dataclass
class UpdateAlbumsTabResponse:
    UpdateAlbumsTabResult: SimpleResult | None


@dataclass
class SetCulture:
    culture: str | None


@dataclass
class SetCultureResponse:
    pass


@dataclass
class TimeSpan:
    pass


@dataclass
class SetTimeZoneOffset:
    offset: TimeSpan


@dataclass
class SetTimeZoneOffsetResponse:
    pass


@dataclass
class SetAutoValidate:
    value: bool


@dataclass
class SetAutoValidateResponse:
    pass


@dataclass
class SetCookies:
    value: str


@dataclass
class SetCookiesResponse:
    pass
