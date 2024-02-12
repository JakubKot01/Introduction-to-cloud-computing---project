from flask import Flask, render_template, request, redirect
from typing import List, Any
from expense import Expense
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"..\Introduction to cloud computing\private key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

expenses_list: list[Expense] = []
categories: list[str] = []
periodicity_list: list[str] = ['daily', 'weekly', 'monthly', 'one-time']

def filter_expenses(category):
    filtered_expenses = []
    if category == 'Wszystkie':
        filtered_expenses = get_expenses()
    else:
        for expense in get_expenses():
            if expense.category == category:
                filtered_expenses.append(expense)
    return filtered_expenses

@app.route('/')
def index():
    if request.method == 'POST':
        selected_category = request.form['category']
        expenses_list = filter_expenses(selected_category)
    else:
        expenses_list = get_expenses()

    categories = get_categories()

    print('expenses_list:')
    for expense in expenses_list:
        print(expense.__getstate__())
    print(f'categories: {categories}')
    return render_template(
        'index.html',
        expenses=expenses_list,
        categories=categories,
        periodicity_list=periodicity_list)

def get_expenses():
    expenses_list = []
    docs = db.collection('expensesCollection').order_by('date', direction=firestore.Query.DESCENDING).stream()

    for doc in docs:
        expense_data = doc.to_dict()
        expenses_list.append(Expense(expense_data['name'], expense_data['amount'], expense_data['category'], expense_data['periodicity'], expense_data['date']))

    return expenses_list

def get_categories():
    categories = []
    doc = db.collection('categories').document('categories').get()
    if doc.exists:
        categories_data = doc.to_dict()
        categories = categories_data['categories']

    return categories


@app.route('/add_expense')
def add_expense():
    return render_template('add_expense.html', categories=categories)


@app.route('/submit_expense', methods=['POST'])
def submit_expense():
    name = request.form['name']
    date = request.form['date']
    amount = request.form['amount']
    category = request.form['category']
    periodicity = request.form['periodicity']

    expenses_list.append(Expense(name, amount, category, periodicity, date))

    # Dodaj nowy wydatek do bazy danych
    db.collection('expensesCollection').add({
        'name': name,
        'date': date,
        'amount': amount,
        'category': category,
        'periodicity': periodicity
    })

    # Przekieruj użytkownika z powrotem na stronę główną
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
