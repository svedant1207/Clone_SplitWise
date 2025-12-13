from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.extensions import db
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.services.split_service import SplitService

expense_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@expense_bp.route("", methods=["GET"])
@login_required
def list_expenses():
    # Show expenses where the user is involved (either paid or split)
    # Since every participant (including payer) has a split, we can just query the splits
    expenses = Expense.query.join(ExpenseSplit).filter(ExpenseSplit.user_id == current_user.id).order_by(Expense.created_at.desc()).all()
    return render_template("expenses.html", expenses=expenses, user=current_user)

# CREATE EXPENSE
@expense_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "POST":
        description = request.form["description"]
        amount = float(request.form["amount"])
        # Get list of friend IDs
        friend_ids = request.form.getlist("friend_ids")
        
        if not friend_ids:
            flash("Please select at least one friend to split with.")
            return redirect(url_for("expenses.add_expense"))

        expense = Expense(
            amount=amount,
            description=description,
            paid_by_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit() # Commit to get ID
        
        # Prepare list of all users involved (current user + selected friends)
        user_ids = [current_user.id] + [int(uid) for uid in friend_ids]
        
        # Use SplitService to split equally
        SplitService.split_equal(expense, user_ids)
        
        flash(f"Expense added and split equally between {len(user_ids)} people!")
        return redirect(url_for("expenses.list_expenses"))
        
    return render_template("add_expense.html", friends=current_user.friends)


# SPLIT EXPENSE
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


# EDIT EXPENSE
@expense_bp.route("/<int:expense_id>/edit", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Only allow payer to edit for now (simplification)
    # Check if user is involved in the expense
    current_user_id = int(current_user.id)
    is_participant = (expense.paid_by_id == current_user_id) or \
                     any(s.user_id == current_user_id for s in expense.splits)
    
    if not is_participant:
        flash("You are not involved in this expense, so you cannot edit it.")
        return redirect(url_for("expenses.list_expenses"))

    if request.method == "POST":
        new_description = request.form["description"]
        new_amount = float(request.form["amount"])
        
        # Get list of friend IDs from form
        friend_ids = request.form.getlist("friend_ids")
        
        expense.description = new_description
        expense.amount = new_amount
        
        # Handle splits
        # If user selected specific friends, we re-split among them + payer
        # If friend_ids list is empty, we might default to just payer (expense of 1)?
        # Or if the form field is missing, maybe they didn't touch it?
        # But we added the field, so it should be there.
        
        if friend_ids:
            # 1. Delete existing splits
            ExpenseSplit.query.filter_by(expense_id=expense.id).delete()
            
            # 2. Create new splits
            user_ids = [current_user.id] + [int(uid) for uid in friend_ids]
            SplitService.split_equal(expense, user_ids)
        
        else:
            pass 
            if not friend_ids:
                 # If we assume checkboxes are present but unchecked -> user removed all friends.
                 # Just split to self?
                 ExpenseSplit.query.filter_by(expense_id=expense.id).delete()
                 SplitService.split_equal(expense, [current_user.id])

        db.session.commit()
        flash("Expense updated!")
        return redirect(url_for("expenses.list_expenses"))
        
    # GET: Prepare data
    # Get IDs of friends currently in the split
    current_participant_ids = [s.user_id for s in expense.splits]
    
    return render_template("edit_expense.html", expense=expense, friends=current_user.friends, current_participant_ids=current_participant_ids)