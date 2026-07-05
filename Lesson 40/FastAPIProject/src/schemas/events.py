from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_serializer
from ..models import UserModel

class EventSchema(BaseModel):
    name: str
    meeting_time: datetime
    description: Optional[str]
    users: List[str]

    model_config = ConfigDict(from_attributes=True) # разрешение создания из любых объектов

    @field_serializer('users')
    def serialize_users(self, users: List[UserModel], _info):
        # Превращаем список объектов UserModel в список их имён
        return [u.username for u in users]