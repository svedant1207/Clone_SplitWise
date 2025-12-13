from app.models.user import User
from app.models.expense import Expense
from app.services.split_service import SplitService
from app.services.balance_service import BalanceService


def test_user_balances_equal_split(session):
    u1 = User(email="payer@test.com", name="Payer")
    u1.set_password("pass")

    u2 = User(email="friend@test.com", name="Friend")
    u2.set_password("pass")

    session.add_all([u1, u2])
    session.commit()

    expense = Expense(amount=100, description="Lunch", paid_by_id=u1.id)
    session.add(expense)
    session.commit()

    SplitService.split_equal(expense, [u1.id, u2.id])

    balances = BalanceService.user_balances()

    # u1 paid 100, owes 50 => +50
    assert balances[u1.id] == 50.0

    # u2 owes 50 => -50
    assert balances[u2.id] == -50.0