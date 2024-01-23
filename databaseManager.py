import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"D:\Desktop\UWr\Introduction to cloud computing\private key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

expenseCategories = ['food', 'taxes', 'subscriptions', 'going out', 'car', 'unexpected']