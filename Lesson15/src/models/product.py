from sqlalchemy import VARCHAR, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, name="id")
    name: Mapped[str] = mapped_column(VARCHAR(255), name="name")
    cost: Mapped[int] = mapped_column(INTEGER, name="cost")
    count: Mapped[int] = mapped_column(INTEGER, name="count")