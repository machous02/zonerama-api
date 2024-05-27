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

    def __init__(self) -> None:
        self._session = Session()
        self._transport = Transport(session=self._session)
        self._client_api = zeep.Client(wsdl=WSDL_API, transport=self._transport)
        self._client_data = zeep.Client(wsdl=WSDL_DATA, transport=self._transport)

    def login(self, email: str, password: str) -> AccountID:
        """Login to Zonerama with an email and a password.

        Args:
            email (str): email
            password (str): password (will be hashed)

        Raises:
            zaexc.ZoneramaAndroidInvalidLoginException: Invalid email
            zaexc.ZoneramaAndroidUnknownAccountID: Unknown email
            zaexc.ZoneramaAndroidWrongPasswordException: Wrong password

        Returns:
            AccountID: The ID of the logged in account
        """
        response = ApiResponse(
            self._client_api.service.Login(
                email, sha256(bytes(password, "utf-8")).hexdigest()
            )
        )

        if not response.success:
            match response.code:
                case "E_ZONERAMA_INVALIDPARAMS":
                    raise zaexc.ZoneramaAndroidInvalidLoginException(
                        response.code, response.message
                    )
                case "E_ZONERAMA_UNKNOWNACCOUNTID":
                    raise zaexc.ZoneramaAndroidUnknownAccountID(
                        response.code, response.message
                    )
                case "E_ZONERAMA_LOGINFAILED":
                    raise zaexc.ZoneramaAndroidWrongPasswordException(
                        response.code, response.message
                    )
                case _:
                    print(response.code)
                    assert False

        self._session.cookies.set(
            "ASP.NET_SessionId",
            self._session.cookies["ASP.NET_SessionId"],
            domain=".zonerama.com",
            path="/",
        )

        assert isinstance(response.result, AccountID)
        return response.result

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

        if not response.success:
            match response.code:
                case "E_ZONERAMA_NEEDLOGIN":
                    raise zaexc.ZoneramaAndroidNotLoggedInException(
                        response.code, response.message
                    )
                case "E_ZONERAMA_UNKNOWNACCOUNTID":
                    raise zaexc.ZoneramaAndroidUnknownAccountID(
                        response.code, response.message
                    )
                case _:
                    print(response.code)
                    assert False

        return AccountInfo(response.result)

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

        if not response.success:
            match response.code:
                case "E_ZONERAMA_NEEDLOGIN":
                    raise zaexc.ZoneramaAndroidNotLoggedInException(
                        response.code, response.message
                    )
                case "E_ZONERAMA_UNKNOWNACCOUNTID":
                    raise zaexc.ZoneramaAndroidUnknownAccountID(
                        response.code, response.message
                    )
                case _:
                    print(response.code)
                    assert False

        if response.result is None:
            raise zaexc.ZoneramaAndroidUnknownAccountID(response.code, response.message)

        return [TabInfo(tab) for tab in response.result.Tab]
