from flask import Flask, render_template, request, redirect, jsonify
from expense import Expense
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from google.cloud import language_v1
from google.oauth2 import service_account


cred = credentials.Certificate(r"..\Introduction-to-cloud-computing\private-key.json")
credentials = service_account.Credentials.from_service_account_file(
    r"..\Introduction-to-cloud-computing\smart-expenses-tracker-414201-8a1571342373.json")
firebase_admin.initialize_app(cred)

client = language_v1.LanguageServiceClient(credentials=credentials)

db = firestore.client()

app = Flask(__name__)

expenses_list: list[Expense] = []
categories: list[str] = []
periodicity_list: list[str] = ['one-time', 'daily', 'weekly', 'monthly', 'yearly']


def get_expenses():
    expenses_list = []
    docs = db.collection('expensesCollection').stream()

    for doc in docs:
        expense_data = doc.to_dict()
        expenses_list.append(
            Expense(expense_data['name'], expense_data['amount'], expense_data['category'],
                    expense_data['periodicity'], expense_data['date'])
        )

    expenses_list.sort(key=lambda x: x.date, reverse=True)

    return expenses_list


def get_categories():
    categories = []
    doc = db.collection('categories').document('categories').get()
    if doc.exists:
        categories_data = doc.to_dict()
        categories = categories_data['categories']

    return categories


def filter_expenses(category, periodicity):
    filtered_expenses = []
    if category == 'All' and periodicity == 'All':
        filtered_expenses = get_expenses()
    else:
        for expense in get_expenses():
            if (expense.category == category and expense.periodicity == periodicity) \
                    or (expense.category == category and expense.periodicity == 'All') \
                    or (expense.category == 'All' and expense.periodicity == periodicity):
                filtered_expenses.append(expense)
    return filtered_expenses


def get_expenses_dict():
    expenses_list = []
    docs = db.collection('expensesCollection').stream()

    for doc in docs:
        expense_data = doc.to_dict()
        expenses_list.append({
            'name': expense_data['name'],
            'amount': expense_data['amount'],
            'category': expense_data['category'],
            'periodicity': expense_data['periodicity'],
            'date': expense_data['date']
        })

    expenses_list.sort(key=lambda x: x['date'], reverse=True)

    return expenses_list


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


@app.route('/add_category', methods=['POST'])
def add_category():
    print(f'request form: {request.form}')
    category_name = request.form['categoryName']
    categories = get_categories()
    print(f'category name: {category_name}')
    print(f'categories: {categories}')
    print(f'db.collection: {db.collection("categories")}')
    categories.append(category_name)

    db.collection('categories').document("categories").update({
        'categories': categories
    })
    return redirect('/')


@app.route('/suggest_category', methods=['POST'])
def suggest_category():
    print('Starting category prediction')
    expense_name = request.form['expenseName']

    document = {"content": expense_name, "type": language_v1.Document.Type.PLAIN_TEXT}
    response = client.analyze_entities(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF32})

    category_mapping = {
        'food': ['dinner', 'lunch', 'breakfast', 'restaurant'],
        'cosmetics': ['shampoo', 'perfume', 'perfumes', 'makeup', 'beauty', 'skincare'],
        'car': ['gas', 'car repair', 'car wash', 'travel'],
        'subscription': ['netflix', 'spotify', 'amazon prime', 'streaming'],
        'bills and fees': ['rent', 'electricity', 'water', 'internet']
    }

    suggested_category = None
    for entity in response.entities:
        print(entity, end='\t')
        for category, keywords in category_mapping.items():
            if any(keyword in entity.name.lower() for keyword in keywords):
                suggested_category = category
                break

    print("")

    if suggested_category is None:
        suggested_category = 'other'

    print(f'Category prediction: {suggested_category}')

    return jsonify({'suggested_category': suggested_category})


@app.route('/stats')
def stats():
    expenses_list = get_expenses_dict()
    print(expenses_list)

    days_of_week_chart = requests.post(
        'https://europe-central2-smart-expenses-tracker-414201.cloudfunctions.net/generate_days_of_week_chart',
        json={'expenses': expenses_list})

    categories_cumulative_chart = requests.post(
        'https://europe-central2-smart-expenses-tracker-414201.cloudfunctions.net/generate_histogram2',
        json={'expenses': expenses_list})

    pie_chart = requests.post(
        'https://europe-central2-smart-expenses-tracker-414201.cloudfunctions.net/generate_histogram3',
        json={'expenses': expenses_list})

    print(f'status codes: {days_of_week_chart.status_code, categories_cumulative_chart.status_code, pie_chart.status_code}')

    if days_of_week_chart.status_code == 200 and categories_cumulative_chart.status_code == 200 and pie_chart.status_code == 200:
        days_of_week_data = days_of_week_chart.json()
        categories_cumulative_chart_data = categories_cumulative_chart.json()
        pie_chart_data = pie_chart.json()

        if 'image' in days_of_week_data and 'image' in categories_cumulative_chart_data and 'image' in pie_chart_data:
            days_of_week_image_data = days_of_week_data['image']
            bar_chart_image_data = categories_cumulative_chart_data['image']
            pie_chart_image_data = pie_chart_data['image']

            return render_template(
                'stats.html',
                histogram_image_data=days_of_week_image_data,
                bar_chart_image_data=bar_chart_image_data,
                pie_chart_image_data=pie_chart_image_data)
        else:
            error_message = 'Error: cannot download charts'
            return render_template('stats.html', error_message=error_message)
    else:
        error_message = 'Error: cannot generate charts'
        return render_template('stats.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
