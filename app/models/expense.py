from app.extensions import db

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    
    # Total amount of the expense
    amount = db.Column(db.Float, nullable=False)
    # Optional note about the expense
    description = db.Column(db.String(255))
    
    # User who paid for the expense
    paid_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    
    paid_by = db.relationship("User", foreign_keys=[paid_by_id])

    # When the expense was created
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # relationship defined on User side (expenses_paid)
    def __repr__(self):
        return f"<Expense {self.id} Amount={self.amount}>"