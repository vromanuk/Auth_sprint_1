from http import HTTPStatus

from flask import request
from flask_apispec import MethodResource, doc, use_kwargs
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from src.database.db import session_scope
from src.schemas.users import UserSchema
from src.services.users_service import UserService


@doc(
    description="users related view, e.g. change-password, change-login",
    tags=["users"],
)
class Users(MethodResource, Resource):
    @use_kwargs(UserSchema)
    @jwt_required()
    def put(self):
        current_user_id = get_jwt_identity()
        try:
            data = {
                "id": current_user_id,
                "login": request.json.get("login", None),
                "password": request.json.get("password", None),
            }
            with session_scope() as session:
                updated_user = UserSchema().load(data, session=session)
        except ValidationError as e:
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST

        is_updated = UserService.update(updated_user)
        if is_updated:
            return {"message": "updated"}, HTTPStatus.OK
        return {"message": f"user not found"}, HTTPStatus.NOT_FOUND
