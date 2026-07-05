from dataclasses import dataclass
from datetime import datetime

from ..models import UserModel

@dataclass(kw_only=True, slots=True)
class UserDTO:
    id: int
    username: str
    password: str
    is_admin: bool
    created_at: datetime

    @classmethod
    def from_model(cls, model: UserModel) -> UserDTO:
        return cls(
            id=model.id,
            username=model.username,
            password=model.password,
            is_admin=model.is_admin,
            created_at=model.created_at,
        )


@dataclass(kw_only=True, slots=True)
class ApiTokenDTO:
    id: int
    user_id: int
    key: str
