from typing import List, Any

from expense import Expense

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"D:\Desktop\UWr\Introduction to cloud computing\private key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

expenses_list: list[Expense] = []

def get_document(collection_name, document_id):
    doc_ref = db.collection(collection_name).document(document_id)
    print(doc_ref)
    doc = doc_ref.get()
    print(doc)

    if doc.exists:
        print(doc)
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
        print(f"Document ID: {doc_data['id']}")
        print(f"Document Data: {doc_data['docData']}")
        print()

        expenses_list.append(
            Expense(
                doc_data['docData']['name'],
                doc_data['docData']['amount'],
                doc_data['docData']['category'],
                doc_data['docData']['periodicity'],
                doc_data['docData']['date']))


categories = get_document('categories', 'categories')
expenseCategories = categories['categories']


def update_categories():
    collection_ref = db.collection('categories')
    doc_ref = collection_ref.document('categories')

    doc_ref.update({
        'categories': expenseCategories
    })
