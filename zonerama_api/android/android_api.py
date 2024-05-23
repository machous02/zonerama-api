from hashlib import sha256

import zeep
from requests import Session
from zeep import Transport

import zonerama_api.android.exceptions as zaexc
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
        response = ApiResponse(
            self._client_api.service.Login(
                email, sha256(bytes(password, "utf-8")).hexdigest()
            )
        )

        if not response.success:
            raise zaexc.ZoneramaAndroidLoginException(response.code, response.message)

        self._session.cookies.set(
            "ASP.NET_SessionId",
            self._session.cookies["ASP.NET_SessionId"],
            domain=".zonerama.com",
            path="/",
        )

        return response.result

    def get_account_info(self, id: AccountID) -> AccountInfo:
        response = ApiResponse(self._client_data.service.GetAccount(id))

        if not response.success:
            raise zaexc.ZoneramaAndroidLoginException(response.code, response.message)

        return AccountInfo(response.result)

    def get_tabs(self, id: AccountID) -> list[TabInfo]:
        response = ApiResponse(self._client_data.service.GetTabs(id))

        if not response.success:
            raise zaexc.ZoneramaAndroidLoginException(response.code, response.message)

        return [TabInfo(tab) for tab in response.result.Tab]
