from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.connector import get_session
from ..exceptions import DomainException, UniqueConstraintError
from ..schemas.auth import AuthUserSchema, LoginUserSchema, ApiTokenSchema
from ..services.auth import create_user_api_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=ApiTokenSchema)
async def login_api_view(data: LoginUserSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        return await create_user_api_token(session, username=data.username, password=data.password)
    except UniqueConstraintError as exc:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    except DomainException as exc:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})


@router.get("/myself", response_model=AuthUserSchema)
async def get_myself_api_view(user: Annotated[AuthUserSchema, Depends(get_current_user)]):
    return user
