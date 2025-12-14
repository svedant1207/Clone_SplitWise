from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        
        if User.query.filter_by(email=email).first():
            flash("Email already exists")
            return redirect(url_for("auth.register"))
        
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for("auth.dashboard"))
        
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            # Handle next parameter for redirection after login
            next_page = request.args.get('next')
            return redirect(next_page or url_for("auth.dashboard"))

        flash("Invalid email or password")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    from app.models.expense import Expense
    from app.models.expense_split import ExpenseSplit
    from app.services.balance_service import BalanceService

    # Recent expenses (last 5 involving current user)
    recent_expenses = (
        Expense.query
        .join(ExpenseSplit)
        .filter(ExpenseSplit.user_id == current_user.id)
        .order_by(Expense.created_at.desc())
        .limit(5)
        .all()
    )

    # Get balances for all users
    balances = BalanceService.user_balances()

    # Current user's net balance
    total_balance = balances.get(current_user.id, 0.0)

    # Calculate owes / owed
    you_owe = 0.0
    you_are_owed = 0.0
    owe_users = set()
    owed_by_users = set()

    for user_id, amount in balances.items():
        if user_id == current_user.id:
            continue

        if amount < 0 and total_balance > 0:
            you_are_owed += abs(amount)
            owed_by_users.add(user_id)

        elif amount > 0 and total_balance < 0:
            you_owe += amount
            owe_users.add(user_id)

    return render_template(
        "dashboard.html",
        user=current_user,
        recent_expenses=recent_expenses,
        total_balance=round(total_balance, 2),
        you_owe=round(you_owe, 2),
        you_are_owed=round(you_are_owed, 2),
        owe_count=len(owe_users),
        owed_by_count=len(owed_by_users),
    )


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))