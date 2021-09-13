from http import HTTPStatus

from psycopg2 import IntegrityError

from src.database.db import session_scope


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
