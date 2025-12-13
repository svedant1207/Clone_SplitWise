from collections import defaultdict
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit


class BalanceService:
    @staticmethod
    def user_balances():
        """
        Returns: dict {user_id: net_amount}
        +ve => gets money, -ve => owes money
        """
        balances = defaultdict(float)

        # Each expense: payer gets full amount
        expenses = Expense.query.all()
        for exp in expenses:
            balances[exp.paid_by_id] += float(exp.amount)

        # Each split: user owes their split
        splits = ExpenseSplit.query.all()
        for split in splits:
            balances[split.user_id] -= float(split.amount)

        # round for currency safety
        return {uid: round(amount, 2) for uid, amount in balances.items()}