from app.models.user import User
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.extensions import db


def test_expense_split_creation(session):
    payer = User(email="payer@split.com", name="Payer")
    payer.set_password("pass")

    friend = User(email="friend@split.com", name="Friend")
    friend.set_password("pass")

    session.add_all([payer, friend])
    session.commit()

    expense = Expense(
        amount=100.0,
        description="Lunch",
        paid_by_id=payer.id
    )

    session.add(expense)
    session.commit()

    split = ExpenseSplit(
        expense_id=expense.id,
        user_id=friend.id,
        amount=50.0
    )

    session.add(split)
    session.commit()

    assert split.id is not None
    assert split.amount == 50.0
    assert split.expense_id == expense.id
    assert split.user_id == friend.id