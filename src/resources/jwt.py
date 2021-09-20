from http import HTTPStatus

from flask import jsonify
from flask_apispec import MethodResource, doc
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource

from src.config import security_params


@doc(description="refresh access token", security=security_params, tags=["refresh"])
class TokenRefresh(MethodResource, Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token), HTTPStatus.OK
