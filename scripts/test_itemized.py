
import os
import sys

# Add app directory to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.expense_item import ExpenseItem
from app.services.split_service import SplitService

def test_itemized():
    app = create_app()
    with app.app_context():
        # Setup
        # Create users
        u1 = User.query.filter_by(email="test1@example.com").first()
        if not u1:
            u1 = User(name="Test1", email="test1@example.com", password_hash="hash")
            db.session.add(u1)
        
        u2 = User.query.filter_by(email="test2@example.com").first()
        if not u2:
            u2 = User(name="Test2", email="test2@example.com", password_hash="hash")
            db.session.add(u2)
            
        db.session.commit()
        
        print(f"User 1 ID: {u1.id}")
        print(f"User 2 ID: {u2.id}")

        # Create Expense for 2 items: 
        # Item A: $10 (u1, u2) -> $5 each
        # Item B: $20 (u2) -> $20 u2
        # Total: $30. u1 should owe $5. u2 should owe $25.
        
        expense = Expense(amount=30.0, description="Itemized Test", paid_by_id=u1.id)
        db.session.add(expense)
        db.session.flush()

        items_data = [
            {"name": "Item A", "amount": 10.0, "user_ids": [u1.id, u2.id]},
            {"name": "Item B", "amount": 20.0, "user_ids": [u2.id]}
        ]
        
        print("Splitting itemized...")
        SplitService.split_itemized(expense, items_data)
        db.session.commit()
        
        # Verify Items
        saved_items = ExpenseItem.query.filter_by(expense_id=expense.id).all()
        print(f"Saved Items: {len(saved_items)}")
        for item in saved_items:
            print(f"- {item.name}: ${item.amount}")
            
        if len(saved_items) != 2:
            print("FAILURE: Incorrect number of items.")
            return

        # Verify Splits
        splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()
        print(f"Saved Splits: {len(splits)}")
        
        u1_split = next((s for s in splits if s.user_id == u1.id), None)
        u2_split = next((s for s in splits if s.user_id == u2.id), None)
        
        print(f"U1 Split: {u1_split.amount if u1_split else 0}")
        print(f"U2 Split: {u2_split.amount if u2_split else 0}")
        
        if u1_split and u1_split.amount == 5.0 and u2_split and u2_split.amount == 25.0:
            print("SUCCESS: Splits calculated correctly.")
        else:
            print("FAILURE: Splits calculation wrong.")

if __name__ == "__main__":
    test_itemized()
