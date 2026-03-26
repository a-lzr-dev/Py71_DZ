from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, name="id")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), name="user_id")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"), name="product_id")
    count: Mapped[int] = mapped_column(INTEGER, name="count")
    order_datetime: Mapped[datetime] = mapped_column(DateTime, name="order_datetime", default=datetime.now())