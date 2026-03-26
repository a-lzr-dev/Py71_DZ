from sqlalchemy import VARCHAR, BOOLEAN, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, name="id")
    uuid: Mapped[str] = mapped_column(VARCHAR(36), name="uuid")
    available: Mapped[bool] = mapped_column(BOOLEAN, name="available", default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), name="user", nullable=True,
                                         default=None)
