import pytest
from app.models.user import User
from app.models.expense import Expense
from app.extensions import db


def test_create_expense(session):
    payer = User(email="payer@example.com", name="Payer")
    payer.set_password("pass")

    session.add(payer)
    session.commit()

    expense = Expense(
        amount=250.0,
        description="Dinner",
        paid_by_id=payer.id
    )

    session.add(expense)
    session.commit()

    assert expense.id is not None
    assert expense.amount == 250.0
    assert expense.paid_by_id == payer.id


def test_expense_requires_amount(session):
    payer = User(email="payer2@example.com", name="Payer2")
    payer.set_password("pass")

    session.add(payer)
    session.commit()

    expense = Expense(
        amount=None,
        description="Invalid Expense",
        paid_by_id=payer.id
    )

    session.add(expense)

    with pytest.raises(Exception):
        session.commit()