import databaseManager
from databaseManager import db

from expenseTrackerApp import ExpenseTrackerApp

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
