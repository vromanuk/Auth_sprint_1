from http import HTTPStatus

from src.database.db import session_scope
from src.database.models import User


class UserService:
    @classmethod
    def update(cls, updated_user) -> tuple[dict, int]:
        user = User.find_by_uuid(updated_user.id)
        if not user:
            return {"message": f"User {user.login} not found"}, HTTPStatus.NOT_FOUND

        with session_scope() as session:
            user.login = updated_user.login
            user.password = updated_user.password
            session.commit()
        return {"message": "Updated successfully"}, HTTPStatus.OK
