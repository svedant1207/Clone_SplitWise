
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.services.settlement_service import SettlementService
from app.services.split_service import SplitService

app = create_app()

with app.app_context():
    print("--- Starting Settlement Verification ---")
    
    # 1. Create Dummy Users if not exist
    user_a = User.query.filter_by(email="verifier_a@example.com").first()
    if not user_a:
        user_a = User(name="Verifier A", email="verifier_a@example.com")
        user_a.set_password("password")
        db.session.add(user_a)
        
    user_b = User.query.filter_by(email="verifier_b@example.com").first()
    if not user_b:
        user_b = User(name="Verifier B", email="verifier_b@example.com")
        user_b.set_password("password")
        db.session.add(user_b)
        
    db.session.commit()
    print(f"Users: {user_a.name} (ID: {user_a.id}), {user_b.name} (ID: {user_b.id})")

    # 2. Cleanup previous test data
    # Find expenses between these two
    expenses = Expense.query.filter(Expense.description == "Verification Expense").all()
    for e in expenses:
        ExpenseSplit.query.filter_by(expense_id=e.id).delete()
        db.session.delete(e)
    db.session.commit()
    print("Cleaned up old verification data.")

    # 3. Create Expense: A pays 100, split equally with B
    expense = Expense(
        amount=100.0,
        description="Verification Expense",
        paid_by_id=user_a.id
    )
    db.session.add(expense)
    db.session.commit()
    
    SplitService.split_equal(expense, [user_a.id, user_b.id])
    print("Created Expense: $100 paid by A, split equally.")

    # 4. Run Settlement
    settlements = SettlementService.settle_up()
    print("\n--- Settlement Results ---")
    
    found_settlement = False
    for s in settlements:
        if s["from"] == user_b.id and s["to"] == user_a.id:
            print(f"SUCCESS: User {s['from']} owes User {s['to']} amount ${s['amount']}")
            if s["amount"] == 50.0:
                print("AMOUNT CHECK: Correct ($50.0)")
                found_settlement = True
            else:
                print(f"AMOUNT CHECK: Incorrect (Expected $50.0, got ${s['amount']})")
    
    if not found_settlement:
        print("FAILURE: Expected settlement not found.")
        print("All Settlements:", settlements)
    else:
        print("\nVerification PASSED.")
