import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"..\Introduction-to-cloud-computing\private-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

batch = db.batch()

expenses_list = [
    {'name': 'Grocery Shopping', 'amount': 100, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-02-02'},
    {'name': 'Haircut', 'amount': 30, 'category': 'cosmetics', 'periodicity': 'one-time', 'date': '2024-02-08'},
    {'name': 'Oil Change', 'amount': 50, 'category': 'car', 'periodicity': 'one-time', 'date': '2024-02-15'},
    {'name': 'Dinner with Friends', 'amount': 50, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-02-05'},
    {'name': 'Restaurant Dinner', 'amount': 60, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-02-10'},
    {'name': 'Christmas Tree', 'amount': 40, 'category': 'other', 'periodicity': 'one-time', 'date': '2024-02-01'},
    {'name': 'Winter Clothes', 'amount': 120, 'category': 'clothing', 'periodicity': 'one-time', 'date': '2024-02-01'},
    {'name': 'Lunch with Colleagues', 'amount': 30, 'category': 'food', 'periodicity': 'one-time',
     'date': '2024-02-15'},
    {'name': 'Home Decor', 'amount': 80, 'category': 'other', 'periodicity': 'one-time', 'date': '2024-02-09'},
    {'name': 'Online Course', 'amount': 70, 'category': 'education', 'periodicity': 'one-time', 'date': '2024-02-14'}
]

for expense in expenses_list:
    doc_ref = db.collection('expensesCollection').document()
    batch.set(doc_ref, expense)

batch.commit()