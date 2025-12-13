from app.services.balance_service import BalanceService


class SettlementService:
    @staticmethod
    def settle_up():
        """
        Returns list of settlements:
        [
          {"from": user_id, "to": user_id, "amount": x}
        ]
        """
        balances = BalanceService.user_balances()

        creditors = []
        debtors = []

        for user_id, amount in balances.items():
            if amount > 0:
                creditors.append([user_id, amount])
            elif amount < 0:
                debtors.append([user_id, -amount])

        settlements = []

        i = j = 0
        while i < len(debtors) and j < len(creditors):
            debtor_id, debt = debtors[i]
            creditor_id, credit = creditors[j]

            settle_amount = min(debt, credit)

            settlements.append({
                "from": debtor_id,
                "to": creditor_id,
                "amount": round(settle_amount, 2)
            })

            debtors[i][1] -= settle_amount
            creditors[j][1] -= settle_amount

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        return settlements