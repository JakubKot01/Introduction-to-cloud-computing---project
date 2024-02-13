from datetime import datetime
from datetime import date as datetype


class Expense:
    EXPENSES = ['daily', 'weekly', 'monthly', 'yearly', 'one-time']

    def __init__(self, name, amount, category, periodicity, date):
        self.name = name
        self.amount = amount
        self.category = category
        self.periodicity = periodicity

        if isinstance(date, datetime):
            self.date = date.date()
        elif isinstance(date, datetype):
            self.date = date
        elif isinstance(date, str):
            self.date = self.parse_date(date)
        else:
            raise ValueError("Invalid date format")

    def parse_date(self, date_str):
        try:
            date_object = datetime.strptime(date_str, '%Y-%m-%d')
            return date_object.date()
        except ValueError:
            print(f'Error parsing date: {date_str}')
            return None