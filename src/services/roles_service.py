from http import HTTPStatus

from src.database.models import Role


class RoleService:
    model = Role

    @classmethod
    def fetch(cls, role_id: int):
        return cls.model.fetch(role_id)

    @classmethod
    def fetch_all(cls):
        return cls.model.fetch_all()

    @classmethod
    def create(cls, role) -> tuple[dict, int]:
        cls.model.create(role)
        return {"message": "created"}, HTTPStatus.CREATED

    @classmethod
    def update(cls, role) -> tuple[dict, int]:
        cls.model.update(role)
        return {"message": "updated"}, HTTPStatus.OK

    @classmethod
    def delete(cls, role_id: int) -> tuple[dict, int]:
        is_deleted = cls.model.delete(role_id)
        if is_deleted:
            return {"message": "deleted"}, HTTPStatus.NO_CONTENT
        return {"message": "not found"}, HTTPStatus.NOT_FOUND
