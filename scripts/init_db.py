import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db


def init_db():
    """
    Initializes the database by creating all tables.
    Run this once before starting the server.
    """
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully")


if __name__ == "__main__":
    init_db()