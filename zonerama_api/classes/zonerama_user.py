from __future__ import annotations

from zonerama_api.gallery import get_username, is_user_id
from zonerama_api.typing import UserId, UserIdentifier, Username


class ZoneramaUser:
    username: Username
    user_id: UserId | None

    def __init__(self, identificator: UserIdentifier) -> None:
        if is_user_id(identificator):
            self.user_id = identificator
            self.username = get_username(identificator)
            return

        self.username = identificator
