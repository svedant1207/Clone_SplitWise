from app.extensions import db

class ExpenseItem(db.Model):
    __tablename__ = "expense_items"

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey("expenses.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # We could store involved users here if we wanted complex item assignment.
    # For now, we'll assume items are just for display/calculation 
    # and the split logic handles creating ExpenseSplits.

    expense = db.relationship("Expense", back_populates="items")

    def __repr__(self):
        return f"<ExpenseItem {self.name} ${self.amount}>"
