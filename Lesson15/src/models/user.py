from sqlalchemy import VARCHAR, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, name="id")
    username: Mapped[str] = mapped_column(VARCHAR(30), unique=True, name="username")
    password: Mapped[str] = mapped_column(VARCHAR(30), name="password")
    points: Mapped[int] = mapped_column(INTEGER, name="points", default=0)