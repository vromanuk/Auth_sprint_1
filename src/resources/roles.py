from http import HTTPStatus

from flask import request
from flask_apispec import MethodResource, doc
from flask_restful import Resource
from pydantic import ValidationError

from src.database.models import Role
from src.schemas.roles import CreateRoleSchema, RoleSchema
from src.services.auth_service import admin_required
from src.services.roles_service import RoleService


@doc(description="CRUD for roles, only available for admin", tags=["roles"])
class RolesResource(MethodResource, Resource):
    schema = RoleSchema
    create_schema = CreateRoleSchema
    model = Role
    service = RoleService

    @admin_required
    def get(self, role_id: int = None):
        if not role_id:
            raw_roles = self.service.fetch_all()
            roles = [self.schema(**role).json() for role in raw_roles]
            return {"result": roles}, HTTPStatus.OK

        role = self.service.fetch(role_id)
        if not role:
            return {"message": "not found"}, HTTPStatus.NOT_FOUND

        return {"result": self.schema(**role).json()}, HTTPStatus.OK

    @admin_required
    def post(self):
        role = self.model(**request.json)
        try:
            self.create_schema.from_orm(role)
        except ValidationError as e:
            return {"message": str(e)}

        is_created = self.service.create(role)
        if is_created:
            return {"message": "created"}, HTTPStatus.CREATED
        return {"message": "something went wrong"}, HTTPStatus.BAD_REQUEST

    @admin_required
    def put(self, role_id: int):
        updated_role = self.model(
            id=role_id,
            name=request.json.get("name"),
            default=request.json.get("default"),
            permissions=request.json.get("permissions"),
        )
        try:
            self.schema.from_orm(updated_role)
        except ValidationError as e:
            return {"message": str(e)}

        is_updated = self.service.update(updated_role)
        if is_updated:
            return {"message": "updated"}, HTTPStatus.OK
        return {"message": "not found"}, HTTPStatus.NOT_FOUND

    @admin_required
    def delete(self, role_id: int):
        is_deleted = self.service.delete(role_id)
        if is_deleted:
            return {"message": "deleted"}, HTTPStatus.NO_CONTENT
        return {"message": "not found"}, HTTPStatus.NOT_FOUND
