from bot import Bot


class CostCategory(Bot):
    """Cost category"""

    def __init__(self, name, current_expenses, limit_expenses):
        self.name = name
        self._current_expenses = current_expenses
        self._limit_expenses = limit_expenses
