from app.extensions import db

class ExpenseSplit(db.Model):
    __tablename__ = "expense_splits"

    id = db.Column(db.Integer, primary_key=True)

    # Which expense this split belongs to
    expense_id = db.Column(
        db.Integer,
        db.ForeignKey("expenses.id"),
        nullable=False
    )

    # Which user this split is assigned to
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Amount owed by the user
    amount = db.Column(db.Float, nullable=False)

    # Relationships for easy access
    expense = db.relationship("Expense", backref="splits")
    user = db.relationship("User", backref="splits")

    def __repr__(self):
        return f"<ExpenseSplit e={self.expense_id} u={self.user_id}>"