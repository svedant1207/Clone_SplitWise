from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    user = User(
        email=data["email"],
        name=data.get("name")
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name
    }), 201