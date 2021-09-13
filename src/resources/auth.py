from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from src.database.models import User
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
        auth = request.authorization
        if not auth:
            return (
                "",
                401,
                {"WWW-Authenticate": "Basic realm='Authentication required'"},
            )
        return AuthService.login(username=auth.get("username", ""), password=auth.get("password", ""))
