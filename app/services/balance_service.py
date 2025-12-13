from collections import defaultdict
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit


class BalanceService:
    @staticmethod
    def user_pairwise_debts():
        """
        Returns a dict of dicts:
        {
            user_id_A: {
                user_id_B: amount_A_owes_B
            }
        }
        Only returns positive debts (A owes B).
        """
        # debts[debtor][creditor] = amount
        debts = defaultdict(lambda: defaultdict(float))

        # We need to look at each expense and its splits
        expenses = Expense.query.all()
        
        for expense in expenses:
            payer_id = expense.paid_by_id
            
            for split in expense.splits:
                if split.user_id == payer_id:
                    continue  # Paying for yourself creates no debt
                
                # split.user_id owes payer_id split.amount
                amount = float(split.amount)
                
                # Add to raw debt
                debts[split.user_id][payer_id] += amount

        # Simplify pairwise
        # If A owes B $10 and B owes A $5 -> A owes B $5
        final_debts = defaultdict(dict)
        
        # Get all unique pairs
        users = set(debts.keys())
        for d in debts.values():
            users.update(d.keys())
        users = list(users)

        processed_pairs = set()

        for i in range(len(users)):
            u1 = users[i]
            for j in range(i + 1, len(users)):
                u2 = users[j]
                
                # Check debt u1 -> u2
                d1 = debts[u1][u2]
                # Check debt u2 -> u1
                d2 = debts[u2][u1]
                
                net = d1 - d2
                
                if net > 0.009: # u1 owes u2
                    final_debts[u1][u2] = round(net, 2)
                elif net < -0.009: # u2 owes u1
                    final_debts[u2][u1] = round(-net, 2)
                    
        return final_debts