from flask import Blueprint, current_app

smoke_bp = Blueprint("smoke", __name__, url_prefix="/v1/smoke/")


@smoke_bp.route("", methods=["GET"])
def smoke():
    current_app.logger.info("smoke check")
    return {"msg": "OK"}
