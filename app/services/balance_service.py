from collections import defaultdict
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit


class BalanceService:
    @staticmethod
    def user_balances():
        """
        Returns:
        {
            user_id: net_balance
        }

        +ve  -> user should receive money
        -ve  -> user owes money
        """

        balances = defaultdict(float)

        # Payer gets full expense amount
        for expense in Expense.query.all():
            balances[expense.paid_by_id] += float(expense.amount)

        # Each split reduces user's balance
        for split in ExpenseSplit.query.all():
            balances[split.user_id] -= float(split.amount)

        return {uid: round(amount, 2) for uid, amount in balances.items()}

    @staticmethod
    def user_pairwise_debts():
        """
        Returns pairwise debts:
        {
            debtor_id: {
                creditor_id: amount
            }
        }

        Only positive debts are returned.
        """
        debts = defaultdict(lambda: defaultdict(float))

        # Build raw debts from expenses
        for expense in Expense.query.all():
            payer_id = expense.paid_by_id

            for split in expense.splits:
                if split.user_id == payer_id:
                    continue  # No debt to self

                debts[split.user_id][payer_id] += float(split.amount)

        # Simplify mutual debts
        final_debts = defaultdict(dict)

        users = set(debts.keys())
        for inner in debts.values():
            users.update(inner.keys())
        users = list(users)

        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                u1, u2 = users[i], users[j]

                d1 = debts[u1][u2]
                d2 = debts[u2][u1]

                net = d1 - d2

                if net > 0.009:
                    final_debts[u1][u2] = round(net, 2)
                elif net < -0.009:
                    final_debts[u2][u1] = round(-net, 2)

        return final_debts