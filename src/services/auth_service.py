from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import create_access_token
from psycopg2 import IntegrityError
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
            return jsonify({"msg": "Incorrect username or password"}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
