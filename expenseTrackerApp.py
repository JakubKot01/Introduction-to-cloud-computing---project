import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

from expense import Expense
from databaseManager import db

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


class AddExpenseWindow(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)

        self.title("Add Expense")
        self.geometry("300x200")

        self.label_name = ttk.Label(self, text="Name:")
        self.entry_name = ttk.Entry(self)

        self.label_amount = ttk.Label(self, text="Amount:")
        self.entry_amount = ttk.Entry(self)

        self.label_category = ttk.Label(self, text="Category:")
        self.entry_category = ttk.Entry(self)

        self.label_periodicity = ttk.Label(self, text="Periodicity:")
        self.combobox_periodicity = ttk.Combobox(self, values=Expense.EXPENSES)

        self.label_date = ttk.Label(self, text="Date:")
        self.entry_date = ttk.Entry(self)

        self.button_add_expense = ttk.Button(self, text="Add Expense", command=self.add_expense)

        self.label_name.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        self.entry_name.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

        self.label_amount.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        self.entry_amount.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

        self.label_category.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
        self.entry_category.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

        self.label_periodicity.grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
        self.combobox_periodicity.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)

        self.label_date.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
        self.entry_date.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

        self.button_add_expense.grid(row=4, column=0, columnspan=2, pady=10)

        self.callback = callback

    def add_expense(self):
        name = self.entry_name.get()
        amount = self.entry_amount.get()
        category = self.entry_category.get()
        periodicity = self.combobox_periodicity.get()
        date = self.entry_date.get()

        if name and amount and category and periodicity and date:
            self.callback(name, amount, category, periodicity, date)
            self.destroy()
        else:
            tk.messagebox.showwarning("Error", "Please fill in all fields.")

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("800x600")

        self.expenses = []

        style = ThemedStyle(self)
        style.set_theme("plastik")

        self.side_menu_frame = ttk.Frame(self, width=150, height=600, style="TFrame")
        self.side_menu_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.listbox = ttk.Treeview(self, columns=("Name", "Amount", "Category", "Periodicity", "Date"), show="headings")
        self.listbox.heading("Name", text="Name")
        self.listbox.heading("Amount", text="Amount")
        self.listbox.heading("Category", text="Category")
        self.listbox.heading("Periodicity", text="Periodicity")
        self.listbox.heading("Date", text="Date")
        self.listbox.grid(row=0, column=1, rowspan=2, pady=10, padx=10, sticky="nsew")

        self.button_add_expense = ttk.Button(self, text="Add Expense", command=self.show_add_expense_window)
        self.button_add_expense.grid(row=2, column=1, pady=10, padx=10, sticky="se")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def switch_view(self, selected_view):
        if selected_view == "Your expenses":
            self.show_expenses_view()
        elif selected_view == "Statistics":
            self.show_statistics_view()

    def show_expenses_view(self):
        # Implementacja wyświetlania widoku z listą wydatków
        print("Showing Your expenses view")

    def show_statistics_view(self):
        # Implementacja wyświetlania widoku ze statystykami
        print("Showing Statistics view")

    def show_add_expense_window(self):
        add_expense_window = AddExpenseWindow(self, self.add_expense)
        add_expense_window.grab_set()

    def add_expense(self, name, amount, category, periodicity, date):
        new_expense = Expense(name, amount, category, periodicity, date)
        self.expenses.append(new_expense)
        self.listbox.insert("", "end", values=(new_expense.name, new_expense.amount, new_expense.category, new_expense.periodicity, new_expense.date))
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

