from http import HTTPStatus

from flask import request
from flask_apispec import MethodResource, doc
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from pydantic import ValidationError

from src.schemas.users import UserSchema
from src.services.users_service import UserService


@doc(
    description="users related view, e.g. change-password, change-login",
    tags=["users"],
)
class Users(MethodResource, Resource):
    @jwt_required()
    def put(self):
        current_user_id = get_jwt_identity()
        try:
            updated_user = UserSchema(
                id=current_user_id,
                login=request.json.get("login", None),
                password=request.json.get("password", None)
            )
        except ValidationError as e:
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST

        msg, code = UserService.update(updated_user)
        return msg, code
