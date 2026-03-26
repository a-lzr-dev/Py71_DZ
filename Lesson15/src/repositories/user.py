from sqlalchemy import select

from . import BaseRepository
from ..config.database import session
from ..models import User, Order, Product


class Users(BaseRepository):

    @staticmethod
    def is_exist(username: str) -> bool:
        # проверка существования пользователя с указанным именем
        query = select(User).where(User.username == username)
        result = session.execute(query).first()
        return result

    @staticmethod
    def registry(username: str, password: str) -> User:
        # регистрация нового пользователя
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def authentification(username: str, password: str) -> User | None:
        # поиск соответствия пользователя параметрам аутентификации
        user = (session.query(User)
                .filter_by(username=username, password=password)
                .first())
        return user

    @staticmethod
    def orders(user: User) -> list[tuple]:
        # получение списка заказов указанного пользователя
        query = (
            select(
                Order.order_datetime.label("order_datetime"),
                Order.count.label("order_count"),
                (Order.count * Product.cost).label("order_sum"),
                Product.name.label("product_name")
            )
            .where(Order.user_id == user.id)
            .join(Product, Order.product_id == Product.id)
        )
        return session.execute(query).all()
