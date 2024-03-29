import datetime
from uuid import UUID

from flask import current_app
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from src import get_redis
from src.database.db import session_scope
from src.database.models import Role, User


class UserService:
    @classmethod
    def update(cls, current_user_id: UUID, updated_user: User) -> bool:
        user = User.find_by_uuid(current_user_id)
        if not user:
            return False

        with session_scope() as session:
            try:
                session.execute(
                    update(User)
                    .where(User.id == current_user_id)
                    .values(login=updated_user.login, password=updated_user.password)
                )
            except IntegrityError:
                session.rollback()
                current_app.logger.info("Cannot update these user")
                return False
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

    @classmethod
    def reset_active_tokens(cls, user_id: UUID) -> None:
        jwt_redis_blocklist = get_redis()
        jwt_redis_blocklist.set(
            f"{user_id}:changed-password",
            str(datetime.datetime.now()),
            ex=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"),
        )
