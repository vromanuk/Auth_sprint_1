from flask_apispec import MethodResource, doc
from flask_restful import Resource


@doc(description="server health check", tags=["smoke"])
class Smoke(MethodResource, Resource):
    def get(self):
        return {"message": "OK"}
