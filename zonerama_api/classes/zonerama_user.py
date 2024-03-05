from __future__ import annotations

from zonerama_api.z_typing import Username, UserId, UserIdentifier
from zonerama_api.api import is_user_id, get_username


class ZoneramaUser:
    username: Username
    user_id: UserId | None

    def __init__(self, identificator: UserIdentifier) -> None:
        if is_user_id(identificator):
            self.user_id = identificator
            self.username = get_username(identificator)
            return

        self.username = identificator
