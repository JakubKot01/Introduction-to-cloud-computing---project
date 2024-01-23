class Expense:
    EXPENSES = ['daily', 'weekly', 'monthly', 'yearly', 'one-time']

    def __init__(self, name, amount, category, periodicity, date):
        self.name = name
        self.amount = amount
        self.category = category
        self.periodicity = periodicity
        self.date = date