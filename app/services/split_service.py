from app.extensions import db
from app.models.expense_split import ExpenseSplit
from app.models.expense_item import ExpenseItem


class SplitService:
    @staticmethod
    def split_equal(expense, user_ids):
        """
        Split expense equally among given users.
        """
        if not user_ids:
            raise ValueError("No users to split expense")

        per_user = round(expense.amount / len(user_ids), 2)
        splits = []

        for user_id in user_ids:
            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount=per_user
            )
            splits.append(split)

        db.session.add_all(splits)
        # Service methods should not commit
        return splits

    @staticmethod
    def split_exact(expense, splits_dict):
        """
        Split expense by exact amounts per user.
        """
        total = round(sum(splits_dict.values()), 2)

        if total != round(expense.amount, 2):
            raise ValueError("Split amounts do not sum to expense total")

        splits = []
        for user_id, amount in splits_dict.items():
            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount=amount
            )
            splits.append(split)

        db.session.add_all(splits)
        # Service methods should not commit
        return splits

    @staticmethod
    def split_percentage(expense, percentage_dict):
        """
        Split expense based on percentage per user.
        """
        total_percentage = sum(percentage_dict.values())

        if total_percentage != 100:
            raise ValueError("Percentages must sum to 100")

        splits = []
        for user_id, percent in percentage_dict.items():
            amount = round(expense.amount * percent / 100, 2)
            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount=amount
            )
            splits.append(split)

        db.session.add_all(splits)
        # Service methods should not commit
        return splits

    @staticmethod
    def split_itemized(expense, items_data):
        """
        Split expense based on items.
        items_data: list of dicts {name, amount, user_ids}
        """
        total_amount = sum(item['amount'] for item in items_data)
        
        # Verify total matches expense amount (allowing small float diff?)
        if abs(total_amount - expense.amount) > 0.01:
             raise ValueError(f"Sum of items ({total_amount}) does not match expense amount ({expense.amount})")

        splits_map = {} # user_id -> amount

        expense_items = []
        for item_data in items_data:
            # Create ExpenseItem
            expense_item = ExpenseItem(
                expense_id=expense.id,
                name=item_data['name'],
                amount=item_data['amount']
            )
            expense_items.append(expense_item)

            # Calculate split for this item
            user_ids = item_data['user_ids']
            if not user_ids:
                continue
                
            per_user = item_data['amount'] / len(user_ids)
            for uid in user_ids:
                splits_map[uid] = splits_map.get(uid, 0) + per_user

        db.session.add_all(expense_items)

        # Create ExpenseSplits
        splits = []
        for user_id, amount in splits_map.items():
            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount=round(amount, 2)
            )
            splits.append(split)
        
        db.session.add_all(splits)
        return splits