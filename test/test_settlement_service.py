from app.models.user import User
from app.models.expense import Expense
from app.services.split_service import SplitService
from app.services.settlement_service import SettlementService


def test_settlement_simple(session):
    u1 = User(email="a@settle.com", name="A")
    u1.set_password("pass")

    u2 = User(email="b@settle.com", name="B")
    u2.set_password("pass")

    u3 = User(email="c@settle.com", name="C")
    u3.set_password("pass")

    session.add_all([u1, u2, u3])
    session.commit()

    # A pays 100 for B and C
    expense = Expense(amount=100, description="Trip", paid_by_id=u1.id)
    session.add(expense)
    session.commit()

    SplitService.split_exact(
        expense,
        {u2.id: 40, u3.id: 60}
    )

    settlements = SettlementService.settle_up()

    assert len(settlements) == 2

    assert {"from": u2.id, "to": u1.id, "amount": 40.0} in settlements
    assert {"from": u3.id, "to": u1.id, "amount": 60.0} in settlements