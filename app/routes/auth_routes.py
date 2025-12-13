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
    
    # Get recent expenses (limit 5)
    recent_expenses = Expense.query.join(ExpenseSplit).filter(
        ExpenseSplit.user_id == current_user.id
    ).order_by(Expense.created_at.desc()).limit(5).all()
    
    return render_template("dashboard.html", user=current_user, recent_expenses=recent_expenses)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))