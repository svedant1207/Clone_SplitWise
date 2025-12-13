from flask import Blueprint, jsonify
from app.services.settlement_service import SettlementService

settlement_bp = Blueprint("settlements", __name__, url_prefix="/settle")


@settlement_bp.route("", methods=["GET"])
def settle_up():
    settlements = SettlementService.settle_up()
    return jsonify(settlements), 200