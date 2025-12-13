import uuid
from app.models.user import User
from app.models.expense import Expense


def setup_users_and_expense(session):
    uid = uuid.uuid4().hex

    u1 = User(email=f"a_{uid}@test.com", name="A")
    u1.set_password("pass")

    u2 = User(email=f"b_{uid}@test.com", name="B")
    u2.set_password("pass")

    session.add_all([u1, u2])
    session.commit()

    expense = Expense(
        amount=100,
        description="Dinner",
        paid_by_id=u1.id
    )

    session.add(expense)
    session.commit()

    return u1, u2, expense