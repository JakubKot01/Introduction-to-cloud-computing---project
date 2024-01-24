import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from expense import Expense
from databaseManager import db
from databaseManager import expenseCategories

from addExpenseWindow import AddExpenseWindow
from addCategoryDialog import AddCategoryDialog


class YourExpensesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        parent.title("Expense Tracker")
        parent.geometry("1400x600")

        parent.listbox = ttk.Treeview(parent, columns=("Name", "Amount", "Category", "Periodicity", "Date"),
                                      show="headings")
        parent.listbox.heading("Name", text="Name")
        parent.listbox.heading("Amount", text="Amount")
        parent.listbox.heading("Category", text="Category")
        parent.listbox.heading("Periodicity", text="Periodicity")
        parent.listbox.heading("Date", text="Date")
        parent.listbox.grid(row=0, column=1, rowspan=2, pady=10, padx=10, sticky="nsew")

        parent.button_add_expense = ttk.Button(parent, text="Add Expense",
                                               command=lambda: self.show_add_expense_window(parent))
        parent.button_add_expense.grid(row=1, column=4, columnspan=2, pady=10, sticky=tk.E + tk.S)

        parent.button_add_category = ttk.Button(parent, text="Add Category", command=self.add_category)
        parent.button_add_category.grid(row=1, column=2, pady=10, padx=10, sticky=tk.E + tk.S)

        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)

        parent.button_view_expenses = ttk.Button(parent, text="Your expenses",
                                                 command=lambda: parent.switch_view("Your expenses"))
        parent.button_view_statistics = ttk.Button(parent, text="Statistics",
                                                   command=lambda: parent.switch_view("Statistics"))

        parent.button_view_expenses.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W + tk.E)
        parent.button_view_statistics.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W + tk.E)

        # Dodajmy kod, aby automatycznie wyświetlić widok Your Expenses po utworzeniu instancji
        # self.show_expenses_view()

    def show_add_expense_window(self, parent):
        add_expense_window = AddExpenseWindow(parent)
        add_expense_window.grab_set()

    def add_category(self):
        dialog = AddCategoryDialog(self, title="Add Category")
        new_category = dialog.result
        if new_category:
            expenseCategories.append(new_category)
            tk.messagebox.showinfo("Success", f"Category '{new_category}' added.")
