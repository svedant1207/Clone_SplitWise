import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db

def reset_db():
    """
    Drops all tables and recreates them.
    Useful during development when schema or data is broken.
    """
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("♻️ Database reset successfully")

if __name__ == "__main__":
    reset_db()