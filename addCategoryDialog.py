import tkinter as tk
from tkinter import ttk, simpledialog


class AddCategoryDialog(simpledialog.Dialog):
    def body(self, master):
        ttk.Label(master, text="New Category:").grid(row=0, sticky=tk.W)
        self.entry_category = ttk.Entry(master)
        self.entry_category.grid(row=0, column=1, sticky=tk.W)
        return self.entry_category

    def apply(self):
        new_category = self.entry_category.get()
        if new_category:
            self.result = new_category
        else:
            self.result = None