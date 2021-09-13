from http import HTTPStatus

from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from src.database.db import session_scope
from src.database.models import User


class AuthService:
    @classmethod
    def register(cls, user) -> tuple[dict, int]:
        with session_scope() as session:
            try:
                session.add(user)
                session.commit()
                return {"message": "Successfully registered"}, HTTPStatus.CREATED
            except IntegrityError:
                session.rollback()
                return {"message": "Such user exists"}, HTTPStatus.CONFLICT

    @classmethod
    def login(cls, username: str, password: str):
        user = User.find_by_username(username)
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid Credentials."}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return (
            {"access_token": access_token, "refresh_token": refresh_token},
            HTTPStatus.OK,
        )
