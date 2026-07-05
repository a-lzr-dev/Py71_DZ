from datetime import datetime

from pydantic import BaseModel, Field

class AuthUserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime

class LoginUserSchema(BaseModel):
    username: str = Field(max_length=64)
    password: str = Field(max_length=64)

class ApiTokenSchema(BaseModel):
    key: str

class TokenResponseSchema(BaseModel):
    api_token: str