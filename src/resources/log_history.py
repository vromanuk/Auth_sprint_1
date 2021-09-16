from http import HTTPStatus

from flask_apispec import MethodResource, doc
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from src.services.log_history_service import LogHistoryService


@doc(description="displays history of user logging sessions", tags=["log-history"])
class LogHistoryResource(MethodResource, Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        log_histories = LogHistoryService.list_histories(current_user_id)
        return {"result": log_histories}, HTTPStatus.OK
