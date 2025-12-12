from flask import Flask
from app.extensions import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/")
    def health_check():
        return {"status": "ok"}

    return app