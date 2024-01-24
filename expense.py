from datetime import datetime
from datetime import date as datetype


class Expense:
    EXPENSES = ['daily', 'weekly', 'monthly', 'yearly', 'one-time']

    def __init__(self, name, amount, category, periodicity, date):
        self.name = name
        self.amount = amount
        self.category = category
        self.periodicity = periodicity

        if type(date) is str:
            self.date = self.parse_date(date)
        else:
            year = date.year
            month = date.month
            day = date.day
            self.date = datetype(year, month, day)

    def parse_date(self, date_str):
        try:
            date_object = datetime.strptime(date_str, '%Y-%m-%d')
            return date_object
        except ValueError:
            print(f'Error parsing date: {date_str}')
            return None