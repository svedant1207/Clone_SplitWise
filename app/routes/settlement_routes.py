from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.settlement_service import SettlementService
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.extensions import db

settlement_bp = Blueprint("settlements", __name__, url_prefix="/settle")


@settlement_bp.route("", methods=["GET"])
@login_required
def settle_view():
    raw_settlements = SettlementService.settle_up()
    
    # Filter for current user and enrich with names
    my_settlements = []
    current_user_id = int(current_user.id)
    
    for s in raw_settlements:
        if s["from"] == current_user_id:
            user = User.query.get(s["to"])
            my_settlements.append({
                "type": "owe",
                "other_user": user,
                "amount": s["amount"]
            })
        elif s["to"] == current_user_id:
            user = User.query.get(s["from"])
            my_settlements.append({
                "type": "owed",
                "other_user": user,
                "amount": s["amount"]
            })
            
    return render_template("settle_up.html", settlements=my_settlements)

@settlement_bp.route("/pay/<int:recipient_id>", methods=["POST"])
@login_required
def make_payment(recipient_id):
    amount = float(request.form["amount"])
    
    # "I pay Recipient" => Expense paid by Me, split to Recipient
    payment = Expense(
        amount=amount,
        description="Settlement Payment",
        paid_by_id=current_user.id
    )
    db.session.add(payment)
    
    split = ExpenseSplit(
        expense=payment,
        user_id=recipient_id,
        amount=amount
    )
    db.session.add(split)
    db.session.commit()
    
    flash(f"Paid ${amount}!")
    return redirect(url_for("settlements.settle_view"))