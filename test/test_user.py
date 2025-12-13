import pytest
from app.models.user import User
from app.extensions import db


def test_password_is_hashed(session):
    user = User(email="test@example.com", name="Test User")
    user.set_password("secret123")

    session.add(user)
    session.commit()

    # password should NOT be stored as plain text
    assert user.password_hash != "secret123"
    assert user.check_password("secret123") is True
    assert user.check_password("wrong") is False


def test_email_must_be_unique(session):
    user1 = User(email="unique@example.com", name="User One")
    user1.set_password("pass")

    user2 = User(email="unique@example.com", name="User Two")
    user2.set_password("pass")

    session.add(user1)
    session.commit()

    session.add(user2)

    with pytest.raises(Exception):
        session.commit()