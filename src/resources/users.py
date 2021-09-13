from http import HTTPStatus

from flask import request
from flask_apispec import MethodResource, doc
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from pydantic import ValidationError

from src.schemas.users import UserSchema
from src.services.users_service import UserService


@doc(
    description="users related view, e.g. change-password, change-username",
    tags=["users"],
)
class Users(MethodResource, Resource):
    @jwt_required()
    def put(self):
        try:
            new_user_info = UserSchema(**request.json)
        except ValidationError as e:
            return {"message": str(e)}
        current_user = get_jwt_identity()
        if current_user.id != new_user_info.id:
            return {
                "message": "Probably, you've specified wrong data"
            }, HTTPStatus.BAD_REQUEST

        msg, code = UserService.update(new_user_info)
        return msg, code