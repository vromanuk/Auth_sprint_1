from http import HTTPStatus

from src.database.db import session_scope
from src.database.models import User


class UserService:
    @classmethod
    def update(cls, updated_user) -> bool:
        user = User.find_by_uuid(updated_user.id)
        if not user:
            return False

        with session_scope() as session:
            user.login = updated_user.login
            user.password = updated_user.password
            session.commit()

        return True
