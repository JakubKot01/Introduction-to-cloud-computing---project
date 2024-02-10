from flask import Flask, render_template
from typing import List, Any
from expense import Expense
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"D:\Desktop\UWr\Introduction to cloud computing\private key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/')
def index():
    expenses_list: list[Expense] = []

    def get_document(collection_name, document_id):
        doc_ref = db.collection(collection_name).document(document_id)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            print(f"Document '{document_id}' not found in collection '{collection_name}'.")
            return None

    def get_all_docs(collectionName):
        docs = (db.collection(collectionName).stream())

        documents_list = []

        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            doc_data['docData'] = doc._data

            documents_list.append(doc_data)

        for doc_data in documents_list:
            expenses_list.append(
                Expense(
                    doc_data['docData']['name'],
                    doc_data['docData']['amount'],
                    doc_data['docData']['category'],
                    doc_data['docData']['periodicity'],
                    doc_data['docData']['date']))

    print(expenses_list)

    categories = get_document('categories', 'categories')
    expenseCategories = categories['categories']

    def update_categories():
        collection_ref = db.collection('categories')
        doc_ref = collection_ref.document('categories')

        doc_ref.update({
            'categories': expenseCategories
        })

    get_all_docs('expensesCollection')
    return render_template('index.html', expenses=expenses_list)

@app.route('/stats')
def stats():
    return render_template('stats.html')

if __name__ == '__main__':
    app.run(debug=True)
