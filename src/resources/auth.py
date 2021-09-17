import datetime
from http import HTTPStatus

from flask import current_app, request
from flask_apispec import MethodResource, doc
from flask_restful import Resource
from marshmallow import ValidationError

from src.database.db import session_scope
from src.database.models import User
from src.schemas.users import UserSchema
from src.services.auth_service import AuthService
from src.services.log_history_service import LogHistoryService


class AuthRegister(MethodResource, Resource):
    user_schema = UserSchema()
    model = User

    @doc(description="user registration view", tags=["register"])
    def post(self):
        try:
            with session_scope() as session:
                user = self.user_schema.load(request.json, session=session)
        except ValidationError as e:
            return {"message": str(e)}
        created = AuthService.register(user)
        if created:
            return {"result": self.user_schema.dump(user)}, HTTPStatus.CREATED
        return {"message": "Such user exists"}, HTTPStatus.CONFLICT


class AuthLogin(MethodResource, Resource):
    @doc(description="user login view", tags=["login"])
    def post(self):
        login = request.json.get("login", None)
        password = request.json.get("password", None)

        logged_in, token = AuthService.login(login=login, password=password)
        if not logged_in:
            return {"message": "Invalid Credentials."}, HTTPStatus.UNAUTHORIZED

        log_history_data = {
            "logged_at": str(datetime.datetime.utcnow()),
            "user_agent": request.user_agent.string,
            "ip": request.remote_addr,
            "user_id": token["user_id"],
            "refresh_token": token["refresh_token"],
            "expires_at": str(
                datetime.datetime.utcnow()
                + current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
            ),
        }
        LogHistoryService.create_entry(log_history_data)

        return token, HTTPStatus.OK
