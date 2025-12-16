from flask import Flask, send_from_directory
from app.extensions import db, login_manager, migrate
from config import Config
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.expense_item import ExpenseItem

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # REQUIRED for sessions
    app.secret_key = app.config["SECRET_KEY"]

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = "auth.login"

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.expense_routes import expense_bp
    from app.routes.balance_routes import balance_bp
    from app.routes.settlement_routes import settlement_bp
    from app.routes.friend_routes import friend_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(balance_bp)
    app.register_blueprint(settlement_bp)
    app.register_blueprint(friend_bp)

    @app.route("/")
    def index():
        return send_from_directory("..", "index.html")

    @app.route("/health")
    def health_check():
        return {"status": "ok"}

    return app