from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.expense import Expense
from app.services.split_service import SplitService

expense_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


# ----------------------------
# CREATE EXPENSE
# ----------------------------
@expense_bp.route("", methods=["POST"])
def create_expense():
    data = request.get_json(force=True)

    # basic validation
    if not all(k in data for k in ("amount", "paid_by_id")):
        return jsonify({"error": "amount and paid_by_id are required"}), 400

    expense = Expense(
        amount=float(data["amount"]),
        description=data.get("description"),
        paid_by_id=int(data["paid_by_id"])
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({
        "id": expense.id,
        "amount": expense.amount,
        "description": expense.description,
        "paid_by_id": expense.paid_by_id
    }), 201


# ----------------------------
# SPLIT EXPENSE
# ----------------------------
@expense_bp.route("/<int:expense_id>/split", methods=["POST"])
def split_expense(expense_id):
    data = request.get_json(force=True)

    if "type" not in data:
        return jsonify({"error": "split type is required"}), 400

    expense = Expense.query.get_or_404(expense_id)
    split_type = data["type"]

    try:
        if split_type == "equal":
            splits = SplitService.split_equal(
                expense,
                data["user_ids"]
            )

        elif split_type == "exact":
            splits = SplitService.split_exact(
                expense,
                data["splits"]
            )

        elif split_type == "percentage":
            splits = SplitService.split_percentage(
                expense,
                data["splits"]
            )

        else:
            return jsonify({"error": "Invalid split type"}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "expense_id": expense.id,
        "splits": [
            {
                "user_id": s.user_id,
                "amount": s.amount
            }
            for s in splits
        ]
    }), 200