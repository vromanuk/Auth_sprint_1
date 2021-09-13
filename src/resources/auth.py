from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from src.database.models import User
from src.schemas.users import UserCreateSchema
from src.services.auth_service import AuthService


class AuthRegister(Resource):
    model = User

    def post(self):
        user_schema = UserCreateSchema()
        try:
            raw_user = User(**request.json)
            user = user_schema.from_orm(raw_user)
        except ValidationError as e:
            return {"message": str(e)}
        msg, code = AuthService.register(user)
        return msg, code
