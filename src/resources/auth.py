import datetime

from flask import request
from flask_apispec import MethodResource, doc
from flask_restful import Resource
from pydantic import ValidationError

from src.database.models import User
from src.schemas.auth import LoginSchema
from src.schemas.users import UserCreateSchema
from src.services.auth_service import AuthService
from src.services.log_history_service import LogHistoryService


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
        login = request.json.get("login", None)
        password = request.json.get("password", None)
        try:
            LoginSchema(login=login, password=password)
        except ValidationError as e:
            return {"message": str(e)}
        msg, code = AuthService.login(login=login, password=password)

        LogHistoryService.create_entry(
            logged_at=datetime.datetime.utcnow(),
            user_agent=request.user_agent.string,
            ip=request.remote_addr,
            user_id=msg["user_id"],
        )

        return msg, code
