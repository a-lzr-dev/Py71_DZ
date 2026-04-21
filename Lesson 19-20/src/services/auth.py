from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

from src.db import db
from src.models import User


class AuthError(Exception): ...


class RegisterError(AuthError): ...


class LoginError(AuthError): ...


def register_user(username: str, password: str) -> None:
    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash)

    if db.session.query(User).filter_by(username=username).first():
        raise RegisterError("Укажите другой username")

    db.session.add(user)
    db.session.commit()


def login_user(username: str, password: str) -> None:
    user = db.session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        raise LoginError("Неверный логин пользователя или пароль")

    session["user_id"] = user.id  # Flask сам всё сделает.


def logout_user() -> None:
    session.pop("user_id", None)  # Flask сам всё сделает.


def get_current_user_from_session() -> User | None:
    user_id = session.get("user_id")
    if user_id is None:
        return None

    return db.session.query(User).filter_by(id=user_id).first()
