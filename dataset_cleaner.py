import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"..\Introduction-to-cloud-computing\private-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

batch = db.batch()

docs = db.collection('expensesCollection').stream()

for doc in docs:
    batch.delete(doc.reference)

batch.commit()