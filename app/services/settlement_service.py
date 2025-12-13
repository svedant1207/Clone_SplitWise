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
        debts = BalanceService.user_pairwise_debts()
        
        settlements = []
        
        for debtor_id, creditors in debts.items():
            for creditor_id, amount in creditors.items():
                if amount > 0:
                    settlements.append({
                        "from": debtor_id,
                        "to": creditor_id,
                        "amount": amount
                    })
                    
        return settlements