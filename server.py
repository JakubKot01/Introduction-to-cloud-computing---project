from flask import Flask, render_template, request, redirect
from typing import List, Any
from expense import Expense
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"..\Introduction-to-cloud-computing\private-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

expenses_list: list[Expense] = []
categories: list[str] = []
periodicity_list: list[str] = ['one-time', 'daily', 'weekly', 'monthly', 'yearly']


def filter_expenses(category, periodicity):
    filtered_expenses = []
    if category == 'Wszystkie' and periodicity == 'Wszystkie':
        filtered_expenses = get_expenses()
    else:
        for expense in get_expenses():
            if (expense.category == category and expense.periodicity == periodicity) \
                    or (expense.category == category and expense.periodicity == 'Wszystkie') \
                    or (expense.category == 'Wszystkie' and expense.periodicity == periodicity):
                filtered_expenses.append(expense)
    return filtered_expenses


@app.route('/')
def index():
    if request.method == 'POST':
        selected_category = request.form['category']
        selected_periodicy = request.form['periodicity']
        expenses_list = filter_expenses(selected_category, selected_periodicy)
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
    docs = db.collection('expensesCollection').stream()

    for doc in docs:
        expense_data = doc.to_dict()
        expenses_list.append(
            Expense(expense_data['name'], expense_data['amount'], expense_data['category'],
                    expense_data['periodicity'], expense_data['date'])
        )

    # Posortuj listę wydatków według daty (od najnowszej do najstarszej)
    expenses_list.sort(key=lambda x: x.date, reverse=True)

    return expenses_list


def get_categories():
    categories = []
    doc = db.collection('categories').document('categories').get()
    if doc.exists:
        categories_data = doc.to_dict()
        categories = categories_data['categories']

    return categories


@app.route('/add_expense', methods=['POST'])
def add_expense():
    name = request.form["expenseName"]
    amount = request.form["expenseAmount"]
    date = request.form["expenseDate"]
    category = request.form["expenseCategory"]
    periodicity = request.form["expensePeriodicity"]
    expenses_list = get_expenses()
    print(name, amount, date, category, periodicity)
    print(f'categories: {expenses_list}')

    expenses_list.append(Expense(name, amount, category, periodicity, date))

    db.collection('expensesCollection').add({
        'name': name,
        'date': date,
        'amount': amount,
        'category': category,
        'periodicity': periodicity
    })

    return redirect('/')


@app.route('/stats')
def stats():
    return render_template('stats.html')


# @app.route('/submit_expense', methods=['POST'])
# def submit_expense():
#     name = request.form['name']
#     date = request.form['date']
#     amount = request.form['amount']
#     category = request.form['category']
#     periodicity = request.form['periodicity']
#
#     expenses_list.append(Expense(name, amount, category, periodicity, date))
#
#     # Dodaj nowy wydatek do bazy danych
#     db.collection('expensesCollection').add({
#         'name': name,
#         'date': date,
#         'amount': amount,
#         'category': category,
#         'periodicity': periodicity
#     })
#
#     # Przekieruj użytkownika z powrotem na stronę główną
#     return redirect('/')

@app.route('/add_category', methods=['POST'])
def add_category():
    print(f'request form: {request.form}')  # Wypisz zawartość formularza
    category_name = request.form['categoryName']
    categories = get_categories()
    print(f'category name: {category_name}')
    print(f'categories: {categories}')
    print(f'db.collection: {db.collection("categories")}')
    categories.append(category_name)
    # Użyj funkcji add(), aby zawsze dodać nowy dokument do kolekcji
    db.collection('categories').document("categories").update({
        'categories': categories
    })
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
