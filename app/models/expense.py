from app.extensions import db

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

    paid_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # relationship defined on User side (expenses_paid)

    def __repr__(self):
        return f"<Expense {self.id} Amount={self.amount}>"