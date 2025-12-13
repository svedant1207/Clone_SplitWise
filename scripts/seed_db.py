import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.expense import Expense
from app.services.split_service import SplitService

def seed_db():
    """
    Populates the database with sample users, an expense,
    and a split. Helpful for quick manual testing.
    """
    app = create_app()
    with app.app_context():
        # Users
        u1 = User(email="a@test.com", name="User A")
        u1.set_password("pass")

        u2 = User(email="b@test.com", name="User B")
        u2.set_password("pass")

        u3 = User(email="c@test.com", name="User C")
        u3.set_password("pass")

        db.session.add_all([u1, u2, u3])
        db.session.commit()

        # Expense
        expense = Expense(amount=100, description="Dinner", paid_by_id=u1.id)
        db.session.add(expense)
        db.session.commit()

        # Split
        SplitService.split_exact(expense, {
            u2.id: 40,
            u3.id: 60
        })

        print("🌱 Database seeded successfully")

if __name__ == "__main__":
    seed_db()