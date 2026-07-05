from typing import Annotated
from fastapi import APIRouter, Depends, responses, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.connector import get_session
from ..exceptions import DomainException, UniqueConstraintError
from ..schemas.auth import AuthUserSchema
from ..schemas.events import EventSchema
from ..services.auth import get_current_user
from ..services.events import find_events, add_user_event

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=list[EventSchema])
async def list_events(session: Annotated[AsyncSession, Depends(get_session)]):
    # Просмотр всех событий (которые еще не начались!)
    try:
        return await find_events(session)
    except UniqueConstraintError as exc:
        return responses.JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    except DomainException as exc:
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})


@router.get("/my", response_model=list[EventSchema])
async def list_events_by_current_user(session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[AuthUserSchema, Depends(get_current_user)]):
    # Просмотр событий, на которые подписан текущий пользователь
    try:
        return await find_events(session, user_id=user.id)
    except UniqueConstraintError as exc:
        return responses.JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    except DomainException as exc:
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})

@router.post("/{event_id}", response_model=EventSchema)
async def subscribe_event(event_id: int, session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[AuthUserSchema, Depends(get_current_user)]):
    # Подписаться на событие, которое еще не началось
    try:
        print(f"event_id={event_id}")
        print(f"user_id={user.id}")
        return await add_user_event(session, event_id=event_id, user_id=user.id)
    except UniqueConstraintError as exc:
        return responses.JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)})
    except DomainException as exc:
        return responses.JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})