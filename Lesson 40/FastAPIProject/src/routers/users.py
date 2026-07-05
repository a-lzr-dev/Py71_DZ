from typing import Annotated
from fastapi import APIRouter, Depends, responses, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.connector import get_session
from ..exceptions import DomainException, UniqueConstraintError
from ..schemas.users import UserSchema, RegisterUserSchema
from ..services.auth import check_user_admin
from ..services.users import create_user, find_users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserSchema)
async def register_user(data: RegisterUserSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    # Регистрации на сайте
    try:
        return await create_user(session, username=data.username, email=data.email, password=data.password)
    except UniqueConstraintError as exc:
        return responses.JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    except DomainException as exc:
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})


@router.get("/", response_model=list[UserSchema], dependencies=[Depends(check_user_admin)])
async def list_users(session: Annotated[AsyncSession, Depends(get_session)]):
    # Просмотр всех зарегистрированных пользователей (только администраторам)
    try:
        return await find_users(session)
    except UniqueConstraintError as exc:
        return responses.JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    except DomainException as exc:
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})
