from app.extensions import db
from app.models.expense_split import ExpenseSplit


class SplitService:
    @staticmethod
    def split_equal(expense, user_ids):
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
        db.session.commit()
        return splits

    @staticmethod
    def split_exact(expense, splits_dict):
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
        db.session.commit()
        return splits

    @staticmethod
    def split_percentage(expense, percentage_dict):
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
        db.session.commit()
        return splits