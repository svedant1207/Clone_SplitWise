from flask import Flask
from app.extensions import db
from config import Config
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    from app.routes.user_routes import user_bp
    from app.routes.expense_routes import expense_bp
    from app.routes.balance_routes import balance_bp
    from app.routes.settlement_routes import settlement_bp  

    app.register_blueprint(user_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(balance_bp)
    app.register_blueprint(settlement_bp)

    @app.route("/")
    def health_check():
        return {"status": "ok"}

    return app