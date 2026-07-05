from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Boolean, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

user_event = Table(
     "user_event",
     Base.metadata,
     Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
     Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
)

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(256))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    events: Mapped[list["EventModel"]] = relationship(secondary=user_event, back_populates="users")

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"User: {self.username}"

class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    meeting_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    users: Mapped[list["UserModel"]] = relationship(secondary=user_event, back_populates="events")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Event: {self.name}"

class APITokenModel(Base):
    __tablename__ = "api_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(128), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_used: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f"APIToken: {self.id}"