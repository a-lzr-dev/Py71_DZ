from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: str = Field(max_length=64)
    password: str = Field(max_length=64)


class RegisterUserSchema(UserSchema):
    email: EmailStr


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True