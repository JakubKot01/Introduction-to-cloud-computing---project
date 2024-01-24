import tkinter as tk
from tkinter import ttk

from tkcalendar import Calendar
from datetime import datetime

from databaseManager import expenseCategories
from expense import Expense

from databaseManager import db


class AddExpenseWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Add Expense")
        self.geometry("350x350")

        self.label_name = ttk.Label(self, text="Name:")
        self.entry_name = ttk.Entry(self)

        self.label_amount = ttk.Label(self, text="Amount:")
        self.entry_amount = ttk.Entry(self)

        self.label_category = ttk.Label(self, text="Category:")
        self.combobox_category = ttk.Combobox(self, values=expenseCategories)

        self.label_periodicity = ttk.Label(self, text="Periodicity:")
        self.combobox_periodicity = ttk.Combobox(self, values=Expense.EXPENSES)

        self.label_date = ttk.Label(self, text="Date:")
        self.label_date.grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)
        self.entry_date = Calendar(self, date_pattern='yyyy-mm-dd')
        self.entry_date.grid(row=4, column=1, pady=5, padx=5, sticky=tk.W)

        self.button_add_expense = ttk.Button(self, text="Add Expense",
                                             command=lambda: self.add_expense(
                                                 parent,
                                                 self.entry_name,
                                                 self.entry_amount,
                                                 self.combobox_category,
                                                 self.combobox_periodicity,
                                                 self.entry_date))

        self.label_name.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        self.entry_name.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

        self.label_amount.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        self.entry_amount.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

        self.label_category.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
        self.combobox_category.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

        self.label_periodicity.grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
        self.combobox_periodicity.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)

        self.label_date.grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)
        self.entry_date.grid(row=4, column=1, pady=5, padx=5, sticky=tk.W)

        self.button_add_expense.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.E + tk.S)

    @staticmethod
    def add_expense(parent, name, amount, category, periodicity, date):
        date = date.get_date()
        new_expense = Expense(name.get(), amount.get(), category.get(), periodicity.get(), date)
        parent.expenses.append(new_expense)
        parent.listbox.insert("", "end", values=(
            new_expense.name, new_expense.amount, new_expense.category, new_expense.periodicity, new_expense.date))
        data = {
            'name': new_expense.name,
            'amount': new_expense.amount,
            'category': new_expense.category,
            'periodicity': new_expense.periodicity,
            'date': new_expense.date
        }

        doc_ref = db.collection('expensesCollection').document()
        doc_ref.set(data)

        print('Document ID: ', doc_ref.id)
