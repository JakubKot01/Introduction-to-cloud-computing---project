import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

from expense import Expense
from yourExpensesView import YourExpensesView

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ttkthemes import ThemedStyle


class ExpenseTrackerApp(tk.Tk):
    def __init__(self):

        self.expenses = []

        super().__init__()

        self.title("Expense Tracker")
        self.geometry("1400x600")

        style = ThemedStyle(self)
        style.set_theme("default")

        self.side_menu_frame = ttk.Frame(self, width=150, height=600, style="TFrame")
        self.side_menu_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.button_view_expenses = ttk.Button(self.side_menu_frame, text="Your expenses",
                                               command=lambda: self.switch_view("Your expenses"))
        self.button_view_statistics = ttk.Button(self.side_menu_frame, text="Statistics",
                                                 command=lambda: self.switch_view("Statistics"))

        self.button_view_expenses.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W + tk.E)
        self.button_view_statistics.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W + tk.E)

    def switch_view(self, selected_view):
        if selected_view == "Your expenses":
            self.show_expenses_view()
        elif selected_view == "Statistics":
            self.show_statistics_view()

    def show_expenses_view(self):
        self.your_expenses_view = YourExpensesView(self)
        self.your_expenses_view.tkraise()
        print("Showing Your expenses view")

    def show_statistics_view(self):
        # Implementacja wyświetlania widoku ze statystykami
        print("Showing Statistics view")

