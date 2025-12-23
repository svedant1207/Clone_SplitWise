
import pytest
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.services.balance_service import BalanceService

def test_dashboard_balance_logic(session):
    # Scenario: 3 Users
    # A pays $300 for dinner with B and C (Split equal: 100 each).
    # Net Balances: A=+200, B=-100, C=-100.
    # Dashboard for A: Should show Owed $200. (B owes 100, C owes 100).
    # Dashboard for B: Should show Owe $100. (Owes A 100).
    
    # Current flawed logic in dashboard route: 
    # For B (Net -100): 
    #   Iterates A (+200): amount > 0 and total_balance (-100) < 0 -> B owes A 200 ??? 
    #   Or maybe it adds A's balance... let's trace:
    #   if amount(200) > 0 and total_balance(-100) < 0: you_owe += 200.
    #   So B's dashboard says "You owe $200" instead of $100. 
    #   AND it might double count if multiple people are involved.
    
    # Setup
    uA = User(email="a@example.com", name="A")
    uA.set_password("p")
    uB = User(email="b@example.com", name="B")
    uB.set_password("p")
    uC = User(email="c@example.com", name="C")
    uC.set_password("p")
    session.add_all([uA, uB, uC])
    session.commit()
    
    # Expense
    expense = Expense(amount=300, description="Dinner", paid_by_id=uA.id)
    session.add(expense)
    session.flush()
    
    splits = [
        ExpenseSplit(expense_id=expense.id, user_id=uA.id, amount=100),
        ExpenseSplit(expense_id=expense.id, user_id=uB.id, amount=100),
        ExpenseSplit(expense_id=expense.id, user_id=uC.id, amount=100)
    ]
    session.add_all(splits)
    session.commit()
    
    # ----------------------------------------------------
    # Replicate Dashboard Logic (Corrected)
    # ----------------------------------------------------
    def calculate_dashboard_stats(current_user):
        balances = BalanceService.user_balances()
        total_balance = balances.get(current_user.id, 0.0)
        
        pairwise_debts = BalanceService.user_pairwise_debts()
        
        you_owe = 0.0
        you_are_owed = 0.0
        
        # 1. Total I owe
        if current_user.id in pairwise_debts:
            for creditor_id, amount in pairwise_debts[current_user.id].items():
                if amount > 0:
                    you_owe += amount

        # 2. Total owed to me
        for debtor_id, debts in pairwise_debts.items():
            if current_user.id in debts:
                 amount = debts[current_user.id]
                 if amount > 0:
                     you_are_owed += amount
                     
        return total_balance, you_owe, you_are_owed

    # Test for User B
    b_total, b_owe, b_owed = calculate_dashboard_stats(uB)
    print(f"User B Stats: Total={b_total}, Owe={b_owe}, Owed={b_owed}")
    
    # User B should Owe 100 to A.
    # Logic now checks pairwise debts: B->A = 100.
    
    assert b_total == -100.0
    assert b_owe == 100.0, f"Expected to owe 100, calculated {b_owe}"
