from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import get_password_hash
from ..db.exception_handler import exception_handler
from ..models import UserModel


async def get_user_by_id(session: AsyncSession, user_id: int) -> UserModel:
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    return result.scalar()

async def find_users(session: AsyncSession, username: str = "") -> list[UserModel]:
     query = select(UserModel).order_by(UserModel.created_at.desc())

     if username:
         query = query.where(UserModel.username == username)

     result = await session.execute(query)

     return list(result.scalars())

async def create_user(session: AsyncSession, *, username: str, email: str, password: str) -> UserModel:
    user = UserModel(username=username, email=email, password=get_password_hash(password))
    session.add(user)
    try:
        await session.commit()
        await session.refresh(user)
    except SQLAlchemyError as exc:
        exception_handler(exc)

    return user