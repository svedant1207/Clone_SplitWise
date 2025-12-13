from flask import Blueprint, jsonify
from app.services.balance_service import BalanceService
from app.services.settlement_service import SettlementService

balance_bp = Blueprint("balances", __name__)


@balance_bp.route("/balances", methods=["GET"])
def get_balances():
    return jsonify(BalanceService.user_balances())


@balance_bp.route("/settlements", methods=["GET"])
def get_settlements():
    return jsonify(SettlementService.settle_up())