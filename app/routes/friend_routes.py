from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.extensions import db

friend_bp = Blueprint("friends", __name__, url_prefix="/friends")

@friend_bp.route("", methods=["GET"])
@login_required
def list_friends():
    return render_template("friends.html", friends=current_user.friends)

@friend_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_friend():
    if request.method == "POST":
        email = request.form["email"]
        friend = User.query.filter_by(email=email).first()
        
        if not friend:
            flash("User not found")
        elif friend == current_user:
            flash("You cannot add yourself as a friend")
        elif current_user.is_friend(friend):
            flash("Already friends")
        else:
            current_user.add_friend(friend)
            db.session.add(friend) # Ensure friend object is tracked
            db.session.commit()
            flash(f"Added {friend.name} as a friend! You are now friends with each other.")
            return redirect(url_for("friends.list_friends"))
            
    return render_template("add_friend.html")
