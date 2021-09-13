from flask import request
from flask_apispec import MethodResource, doc
from flask_restful import Resource
from pydantic import ValidationError

from src.database.models import User
from src.schemas.auth import LoginSchema
from src.schemas.users import UserCreateSchema
from src.services.auth_service import AuthService


class AuthRegister(MethodResource, Resource):
    model = User

    @doc(description="user registration view", tags=["register"])
    def post(self):
        try:
            login = request.json.get("login", None)
            password = request.json.get("password", None)
            raw_user = self.model(login=login, password=password, is_admin=False)
            UserCreateSchema.from_orm(raw_user)
        except ValidationError as e:
            return {"message": str(e)}
        msg, code = AuthService.register(raw_user)
        return msg, code


class AuthLogin(MethodResource, Resource):
    @doc(description="user login view", tags=["login"])
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        try:
            LoginSchema(username=username, password=password)
        except ValidationError as e:
            return {"message": str(e)}
        msg, code = AuthService.login(username=username, password=password)
        return msg, code
