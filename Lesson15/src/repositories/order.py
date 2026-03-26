from . import BaseRepository
from ..config.database import session
from ..models import User, Order, Product

class InsufficientProductError(Exception):
    """Товара нет в нужном количестве."""
    pass

class InsufficientPointsError(Exception):
    """Недостаточно баллов для покупки."""
    pass

class OrderRepository(BaseRepository):

    @staticmethod
    def create_order(user: User, product: Product, count: int) -> int:
        # покупка товара
        if product.count < count:
            raise InsufficientProductError(
                f"Недостаточно товара '{product.name}'. Доступно: {product.count}, запрошено: {count}"
            )
        total_cost = count * product.cost
        if user.points < total_cost:  # есть в наличие товары и средства для покупки
            raise InsufficientPointsError(
                f"Недостаточно поинтов. Требуется: {total_cost}, доступно: {user.points}"
            )

        order = Order(user_id=user.id, product_id=product.id, count=count)
        user.points -=  total_cost
        product.count -= count
        session.add(order)
        session.commit()
        return order.id