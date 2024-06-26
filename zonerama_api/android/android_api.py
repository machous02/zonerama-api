from __future__ import annotations

from hashlib import sha256

import zeep
from requests import Session
from zeep import Transport

import zonerama_api.android.android_exceptions as zaexc
from zonerama_api.android.android_typing import (
    AccountID,
    AccountInfo,
    ApiResponse,
    TabInfo,
    TabID,
    AlbumInfo,
    AlbumID,
)

WSDL_API = "http://zonerama.com/services/android/apiservice.asmx?WSDL"
WSDL_DATA = "http://zonerama.com/services/android/dataservice.asmx?WSDL"

### DOCUMENTATION: http://zonerama.com/services/android/dataservice.asmx
###                http://zonerama.com/services/android/apiservice.asmx


class Client:
    _session: Session
    _transport: Transport
    _client_api: zeep.Client
    _client_data: zeep.Client
    email: str
    password: str
    logged_in: bool = False
    logged_in_as: AccountID | None = None

    def __init__(self, email: str, password: str) -> None:
        self._session = Session()
        self._transport = Transport(session=self._session)
        self._client_api = zeep.Client(wsdl=WSDL_API, transport=self._transport)
        self._client_data = zeep.Client(wsdl=WSDL_DATA, transport=self._transport)
        self.email = email
        self.password = password

    def __enter__(self) -> Client:
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.logout()

    def login(self) -> None:
        """Login to Zonerama with the stored email and a password.

        Raises:
            zaexc.ZoneramaAndroidInvalidLoginException: Invalid email
            zaexc.ZoneramaAndroidUnknownAccountID: Unknown email
            zaexc.ZoneramaAndroidWrongPasswordException: Wrong password
        """
        response = ApiResponse(
            self._client_api.service.Login(
                self.email, sha256(bytes(self.password, "utf-8")).hexdigest()
            )
        )

        response.raise_for_code()

        # Otherwise the cookie will not be sent
        self._session.cookies.set(
            "ASP.NET_SessionId",
            self._session.cookies["ASP.NET_SessionId"],
            domain=".zonerama.com",
            path="/",
        )

        assert isinstance(response.result, AccountID)

        self.logged_in = True
        self.logged_in_as = response.result

    def logout(self) -> None:
        """Log out of the open session.

        Raises:
            zaexc.ZoneramaAndroidNotLoggedInException: Not logged in
        """
        response = ApiResponse(self._client_api.service.Logout())

        response.raise_for_code()

        self.logged_in = False
        self.logged_in_as = None

    def get_account_info(self, id: AccountID) -> AccountInfo:
        """Get info for an account of the given ID.

        Args:
            id (AccountID): ID of the account

        Raises:
            zaexc.ZoneramaAndroidNotLoggedInException: Not logged in
            zaexc.ZoneramaAndroidUnknownAccountID: Unknown account id

        Returns:
            AccountInfo: The AccountInfo object for the account with the id.
        """
        response = ApiResponse(self._client_data.service.GetAccount(id))

        response.raise_for_code()

        return AccountInfo(response.result)

    def get_tab(self, id: TabID) -> TabInfo:
        """Get a tab of the given ID.

        Args:
            id (TabID): The ID of the tab

        Raises:
            zaexc.ZoneramaAndroidNotLoggedInException: Not logged in
            zaexc.ZoneramaAndroidUnknownTabID: Unknown tab id
            zaexc.ZoneramaAndroidAccessDenied: Access denied

        Returns:
            TabInfo: A TabInfo object for the specified tab
        """
        response = ApiResponse(self._client_data.service.GetTab(id))

        response.raise_for_code()

        return TabInfo(response.result)

    def get_tabs(self, id: AccountID) -> list[TabInfo]:
        """Get tabs of the account with the given ID. \
            Private tabs will be listed only when id is of the account logged in.

        Args:
            id (AccountID): ID of the account

        Raises:
            zaexc.ZoneramaAndroidNotLoggedInException: Not logged in
            zaexc.ZoneramaAndroidUnknownAccountID: Unknown account id

        Returns:
            list[TabInfo]: A list of TabInfo object for each tab.
        """
        response = ApiResponse(self._client_data.service.GetTabs(id))

        response.raise_for_code()

        if response.result is None:
            raise zaexc.ZoneramaAndroidUnknownAccountID(response.code, response.message)

        return [TabInfo(tab) for tab in response.result.Tab]

    def get_album(self, id: AlbumID) -> AlbumInfo:
        """Get an album of the given ID.

        Args:
            id (AlbumID): The ID of the album

        Raises:
             zaexc.ZoneramaAndroidNotLoggedInException: Not logged in
             zaexc.ZoneramaAndroidUnknownAlbumID: Unknown album id
             zaexc.ZoneramaAndroidAccessDenied: Access denied

        Returns:
            AlbumInfo: An AlbumInfo object for the specified album
        """
        response = ApiResponse(self._client_data.service.GetAlbum(id))

        response.raise_for_code()

        return AlbumInfo(response.result)

    def get_albums_in_account(self, id: AccountID) -> list[AlbumInfo]:
        """Get albums of the account with the given ID. \
            Private albums will be listed only when id is of the account logged in.

        Args:
            id (AccountID): The ID of the account

        Raises:
             zaexc.ZoneramaAndroidNotLoggedInException: Not logged in
             zaexc.ZoneramaAndroidUnknownAccountID: Unknown account id

        Returns:
            list[AlbumInfo]: A list of AlbumInfo object for each album.
        """
        response = ApiResponse(self._client_data.service.GetAlbums(id))

        response.raise_for_code()

        return [AlbumInfo(album) for album in response.result.Album]

    def get_albums_in_tab(self, id: TabID) -> list[AlbumInfo]:
        """Get albums in the tab with the given ID.
        Args:
            id (TabID): The ID of the tab

        Raises:
             zaexc.ZoneramaAndroidNotLoggedInException: Not logged in
             zaexc.ZoneramaAndroidUnknownTabID: Unknown account id
             zaexc.ZoneramaAndroidAccessDenied: Access denied

        Returns:
            list[AlbumInfo]: A list of AlbumInfo object for each album.
        """
        response = ApiResponse(self._client_data.service.GetAlbumsInTab(id))

        response.raise_for_code()

        if response.result is None:
            return []

        return [AlbumInfo(album) for album in response.result.Album]
