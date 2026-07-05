from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..exceptions import DomainException
from ..db.exception_handler import exception_handler
from ..models import EventModel
from ..services.users import get_user_by_id

async def get_event_by_id(session: AsyncSession, event_id: int) -> EventModel:
    query = select(EventModel).where(EventModel.id == event_id)
    result = await session.execute(query)
    return result.scalar()

async def find_events(session: AsyncSession, *, user_id: None | int = None, actual: bool = True) -> list[EventModel]:
    query = select(EventModel).order_by(EventModel.meeting_time.asc())

    if user_id:
        query = query.where(EventModel.users.any(id=user_id))

    if actual:
        now = datetime.now()
        query = query.where(EventModel.meeting_time > now)

    query = query.options(selectinload(EventModel.users))

    result = await session.execute(query)

    return list(result.scalars())


async def add_user_event(session: AsyncSession, *, event_id: int, user_id: int) -> EventModel:
    stmt = select(EventModel).where(EventModel.id == event_id).options(selectinload(EventModel.users))
    result = await session.execute(stmt)
    event = result.scalar_one_or_none()
    if event is None:
        raise ValueError(f"Событие с ID {event_id} не найдено")

    user = await get_user_by_id(session, user_id)
    if user is None:
        raise ValueError(f"Пользователь с ID {user_id} не найден")

    if user in event.users:
        raise DomainException(f"Пользователь уже подписан на событие с ID {event_id}")

    event.users.append(user)

    try:
        await session.commit()
        await session.refresh(event)
    except SQLAlchemyError as exc:
        exception_handler(exc)

    return event