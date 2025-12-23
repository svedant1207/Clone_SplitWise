
import pytest
import json
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit

def test_add_expense_invalid_amount_crash(client, session):
    # Setup User and Login
    user1 = User(email="crush@example.com", name="Crush")
    user1.set_password("password")
    session.add(user1)
    session.commit()

    client.post("/login", data={
        "email": "crush@example.com",
        "password": "password"
    }, follow_redirects=True)

    # Submit with empty amount - mimic user error or frontend sync failure
    # This should ideally handle gracefully, but we suspect it crashes (500)
    # or raises ValueError that isn't caught.
    # We expect 500 if our hypothesis is correct that it's uncaught.
    # Or checking if it raises exception.
    
    # client.post swallows exceptions unless we check return code or configure app to propagate.
    # Helper:
    response = client.post("/expenses/add", data={
        "description": "Crash Party",
        "amount": "", # Invalid float
        "split_type": "equal",
        "friend_ids": []
    }, follow_redirects=True)
    
    # If it crashes, status code is 500.
    # If it is handled (caught), it might redirect to add_expense (200).
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 500:
        print("Confirmed: App crashes with 500 on invalid amount.")
    elif response.status_code == 200:
        # Check if it rendered "Error"
        if "Error" in response.get_data(as_text=True):
             print("Handled: Error message shown.")
        else:
             print("Unknown state. Maybe accepted?")

    assert response.status_code != 500, "App should not crash on invalid input"
