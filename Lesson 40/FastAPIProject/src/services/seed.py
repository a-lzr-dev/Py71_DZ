from faker import Faker
from sqlalchemy import select, func, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.exception_handler import exception_handler
from ..services.auth import get_password_hash
from ..models import UserModel, EventModel

fake = Faker()


async def generate_test_data(session: AsyncSession) -> None:
    # генерация тестовых данных
    try:
        stmt_count = select(func.count()).select_from(UserModel)
        result = await session.execute(stmt_count)
        user_count = result.scalar()

        # генерация пользователей
        if user_count == 0:
            users_data = [
                {
                    "username": "admin",
                    "email": "admin@localhost",
                    "password": get_password_hash("admin!"),
                }
            ]
            for _ in range(10):
                users_data.append({
                    "username": fake.name(),
                    "email": fake.unique.email(),
                    "password": get_password_hash(fake.password()),
                })
            await session.execute(insert(UserModel), users_data)

        # генерация событий
        events_data = []
        for _ in range(10):
            events_data.append({
                "name": fake.name(),
                "meeting_time": fake.date_time_between(start_date="-1h", end_date="+40h"),
                "description": fake.text(max_nb_chars=200),
            })
        await session.execute(insert(EventModel), events_data)

        await session.commit()

        print("✅ Тестовые данные успешно сгенерированы")
    except SQLAlchemyError as exc:
        exception_handler(exc)