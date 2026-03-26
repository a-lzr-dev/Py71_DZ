from sqlalchemy import select

from . import BaseRepository
from ..config.database import session
from ..models import Product

class Products(BaseRepository):

    @staticmethod
    def get_products() -> list[Product]:
        # загрузка списка продуктов
        query = select(Product)
        return session.execute(query).scalars().all()

    @staticmethod
    def get_by_id(product_id: int) -> Product:
        # получение товара по id записи
        product = (session.query(Product)
                .filter_by(id=product_id)
                .first())
        return product