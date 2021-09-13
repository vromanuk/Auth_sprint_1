from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from src.database.models import User
from src.schemas.auth import LoginSchema
from src.schemas.users import UserCreateSchema
from src.services.auth_service import AuthService


class AuthRegister(Resource):
    model = User

    def post(self):
        try:
            raw_user = self.model(**request.json)
            user = UserCreateSchema.from_orm(raw_user)
        except ValidationError as e:
            return {"message": str(e)}
        msg, code = AuthService.register(user)
        return msg, code


class AuthLogin(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        try:
            LoginSchema(username=username, password=password)
        except ValidationError as e:
            return {"message": str(e)}
        return AuthService.login(username=username, password=password)
