from http import HTTPStatus
from uuid import UUID

from sqlalchemy import update

from src.database.db import session_scope
from src.database.models import Role, User


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

    @classmethod
    def update_role(cls, user_id: UUID, role_id: int) -> bool:
        user = User.find_by_uuid(user_id)
        if not user:
            return False

        role = Role.fetch(role_id)
        if not role:
            return False

        with session_scope() as session:
            session.execute(
                update(User).where(User.id == user_id).values(role_id=role_id)
            )

        return True

    @classmethod
    def reset_role(cls, user_id: UUID) -> bool:
        user = User.find_by_uuid(user_id)
        if not user:
            return False

        with session_scope() as session:
            session.execute(update(User).where(User.id == user_id).values(role_id=None))

        return True
