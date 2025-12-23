
import pytest
import json
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.expense_item import ExpenseItem

def test_add_expense_itemized_flow(client, session):
    # 1. Setup Data
    user1 = User(email="user1@example.com", name="User1")
    user1.set_password("password")
    user2 = User(email="user2@example.com", name="User2")
    user2.set_password("password")
    session.add_all([user1, user2])
    session.commit()
    
    # Refresh to get IDs
    user1_id = user1.id
    user2_id = user2.id

    # Make them friends
    user1.friends.append(user2)
    session.commit()

    # 2. Login
    client.post("/login", data={
        "email": "user1@example.com",
        "password": "password"
    }, follow_redirects=True)

    # 3. Prepare Itemized Data
    # 2 Items:
    # Item 1: "Pizza", $20.00, Split by User1 and User2
    # Item 2: "Drinks", $10.00, Split by User1 only
    # Total: $30.00
    
    items = [
        {
            "name": "Pizza",
            "amount": 20.00,
            "user_ids": [user1_id, user2_id]
        },
        {
            "name": "Drinks",
            "amount": 10.00,
            "user_ids": [user1_id]
        }
    ]
    
    items_json = json.dumps(items)

    # 4. Submit Form
    response = client.post("/expenses/add", data={
        "description": "Party",
        "amount": "30.00",
        "split_type": "itemized",
        "items_data": items_json,
        # friend_ids might be sent even for itemized, or not. 
        # The form has them but hidden/shown based on split type.
        # But itemized logic doesn't seemingly rely on them.
    }, follow_redirects=True)

    # 5. Check response
    assert response.status_code == 200
    response_text = response.get_data(as_text=True)
    if "Itemized expense added successfully" not in response_text:
        print("FAILED TO ADD EXPENSE. RESPONSE CONTENT:")
        # Print only the flash messages if possible, or body
        print(response_text)
        
    assert "Itemized expense added successfully" in response_text

    # 6. Verify Database
    expense = Expense.query.filter_by(description="Party").first()
    assert expense is not None
    assert expense.amount == 30.00
    assert len(expense.items) == 2
    
    # Check splits
    # Item 1: $20. U1=$10, U2=$10
    # Item 2: $10. U1=$10
    # Total U1 = $20, Total U2 = $10
    
    splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()
    u1_split = next(s for s in splits if s.user_id == user1_id)
    u2_split = next(s for s in splits if s.user_id == user2_id)
    
    assert u1_split.amount == 20.00
    assert u2_split.amount == 10.00
