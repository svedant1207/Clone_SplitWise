
import sys
import os
import random
from datetime import datetime, timedelta

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit

def add_test_data(target_email="test@example.com"):
    app = create_app()
    with app.app_context():
        # 1. Get Target User
        target_user = User.query.filter_by(email=target_email).first()
        if not target_user:
            print(f"User with email {target_email} not found. Creating one...")
            target_user = User(
                name="Test User", 
                email=target_email, 
                mobile_number="1234567890"
            )
            target_user.set_password("password123")
            db.session.add(target_user)
            db.session.commit()
            print(f"Created user: {target_user.email} (password: password123)")

        print(f"Adding friends to: {target_user.name} ({target_user.email})")

        # 2. Create Random Friends
        new_friends = []
        for i in range(5):
            # Generate random suffix to avoid collisions if run multiple times
            suffix = random.randint(1000, 9999)
            friend_name = f"Friend {suffix}"
            friend_email = f"friend{suffix}@example.com"
            
            friend = User(
                name=friend_name,
                email=friend_email,
                mobile_number=f"555{suffix}"
            )
            friend.set_password("password")
            db.session.add(friend)
            new_friends.append(friend)
        
        db.session.commit()
        
        # 3. Add Friends and Create Expenses
        for friend in new_friends:
            # Add as friend
            target_user.add_friend(friend)
            
            # Create a random expense
            amount = round(random.uniform(10.0, 100.0), 2)
            desc = random.choice([
                "Lunch", "Dinner", "Movies", "Drinks", "Taxi", "Groceries", "Concert"
            ])
            
            # 50% chance target paid, 50% chance friend paid
            payer = target_user if random.choice([True, False]) else friend
            
            expense = Expense(
                amount=amount,
                description=f"{desc} with {friend.name}",
                paid_by_id=payer.id,
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(expense)
            
            # Split equally
            split_amount = amount / 2
            split1 = ExpenseSplit(expense=expense, user_id=target_user.id, amount=split_amount)
            split2 = ExpenseSplit(expense=expense, user_id=friend.id, amount=split_amount)
            db.session.add_all([split1, split2])
            
            print(f"  Added friend {friend.name} and expense '${amount}' ({desc})")

        db.session.commit()
        print("Done! Added 5 friends and 5 expenses.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        add_test_data(sys.argv[1])
    else:
        add_test_data()
