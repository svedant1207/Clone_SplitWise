
import os
import sys

# Add app directory to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.services.split_service import SplitService

def reproduce_bug():
    app = create_app()
    with app.app_context():
        # Setup
        db.create_all()
        
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
        
        # Create Expense
        expense = Expense(amount=100.0, description="Original", paid_by_id=u1.id)
        db.session.add(expense)
        db.session.commit()
        
        SplitService.split_equal(expense, [u1.id, u2.id])
        
        print(f"Original Expense: Amount={expense.amount}, Desc={expense.description}")
        
        # Simulate Edit - similar to route logic
        # 1. Update expense fields
        expense.description = "Updated"
        expense.amount = 200.0
        
        # 2. Update splits (using logic from route)
        ExpenseSplit.query.filter_by(expense_id=expense.id).delete()
        SplitService.split_equal(expense, [u1.id, u2.id])
        
        # 3. Commit
        db.session.commit()
        
        # Refetch
        db.session.refresh(expense)
        print(f"Updated Expense: Amount={expense.amount}, Desc={expense.description}")
        
        if expense.amount == 200.0 and expense.description == "Updated":
            print("SUCCESS: Expense updated correctly.")
        else:
            print("FAILURE: Expense did not update correctly.")

if __name__ == "__main__":
    reproduce_bug()
