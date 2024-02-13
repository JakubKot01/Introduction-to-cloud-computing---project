import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"..\Introduction-to-cloud-computing\private-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

batch = db.batch()

expenses_list = [
{'name': 'Grocery Shopping', 'amount': 100, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-02-10'},
    {'name': 'Lunch', 'amount': 15, 'category': 'food', 'periodicity': 'daily', 'date': '2024-02-09'},
    {'name': 'Car Wash', 'amount': 20, 'category': 'car', 'periodicity': 'weekly', 'date': '2024-02-08'},
    {'name': 'Netflix Subscription', 'amount': 12, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-02-07'},
    {'name': 'Electricity Bill', 'amount': 80, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-02-06'},
    {'name': 'Dinner at Restaurant', 'amount': 50, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-02-05'},
    {'name': 'Cosmetic Products', 'amount': 30, 'category': 'cosmetics', 'periodicity': 'one-time', 'date': '2024-02-04'},
    {'name': 'Car Maintenance', 'amount': 200, 'category': 'car', 'periodicity': 'yearly', 'date': '2024-02-03'},
    {'name': 'Magazine Subscription', 'amount': 25, 'category': 'subscription', 'periodicity': 'yearly', 'date': '2024-02-02'},
    {'name': 'Internet Bill', 'amount': 60, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-02-01'},
    {'name': 'Dinner Ingredients', 'amount': 30, 'category': 'food', 'periodicity': 'weekly', 'date': '2024-01-31'},
    {'name': 'Face Cream', 'amount': 20, 'category': 'cosmetics', 'periodicity': 'one-time', 'date': '2024-01-30'},
    {'name': 'Car Insurance', 'amount': 500, 'category': 'car', 'periodicity': 'yearly', 'date': '2024-01-29'},
    {'name': 'Streaming Service', 'amount': 15, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-28'},
    {'name': 'Mobile Phone Bill', 'amount': 40, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-01-27'},
    {'name': 'Takeout Dinner', 'amount': 40, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-01-26'},
    {'name': 'Shampoo', 'amount': 10, 'category': 'cosmetics', 'periodicity': 'monthly', 'date': '2024-01-25'},
    {'name': 'Car Registration Renewal', 'amount': 150, 'category': 'car', 'periodicity': 'yearly', 'date': '2024-01-24'},
    {'name': 'Gym Membership', 'amount': 50, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-23'},
    {'name': 'Water Bill', 'amount': 30, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-01-22'},
    {'name': 'Fast Food', 'amount': 20, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-01-21'},
    {'name': 'Facial Cleanser', 'amount': 15, 'category': 'cosmetics', 'periodicity': 'monthly', 'date': '2024-01-20'},
    {'name': 'Fuel', 'amount': 50, 'category': 'car', 'periodicity': 'weekly', 'date': '2024-01-19'},
    {'name': 'Music Streaming', 'amount': 10, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-18'},
    {'name': 'Insurance Premium', 'amount': 100, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-01-17'},
    {'name': 'Brunch', 'amount': 30, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-01-16'},
    {'name': 'Hair Conditioner', 'amount': 12, 'category': 'cosmetics', 'periodicity': 'monthly', 'date': '2024-01-15'},
    {'name': 'Parking Fee', 'amount': 5, 'category': 'car', 'periodicity': 'one-time', 'date': '2024-01-14'},
    {'name': 'Movie Rental', 'amount': 3, 'category': 'subscription', 'periodicity': 'one-time', 'date': '2024-01-13'},
    {'name': 'Trash Collection', 'amount': 15, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-01-12'},
    {'name': 'Dinner Reservation', 'amount': 40, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-01-11'},
    {'name': 'Hand Cream', 'amount': 8, 'category': 'cosmetics', 'periodicity': 'one-time', 'date': '2024-01-10'},
    {'name': 'Car Maintenance', 'amount': 100, 'category': 'car', 'periodicity': 'monthly', 'date': '2024-01-09'},
    {'name': 'Online Course Subscription', 'amount': 30, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-08'},
    {'name': 'Internet Installation', 'amount': 50, 'category': 'bills and fees', 'periodicity': 'one-time', 'date': '2024-01-07'},
    {'name': 'Coffee', 'amount': 5, 'category': 'food', 'periodicity': 'daily', 'date': '2024-01-06'},
    {'name': 'Makeup Remover', 'amount': 10, 'category': 'cosmetics', 'periodicity': 'monthly', 'date': '2024-01-05'},
    {'name': 'Car Inspection', 'amount': 70, 'category': 'car', 'periodicity': 'yearly', 'date': '2024-01-04'},
    {'name': 'E-book Subscription', 'amount': 15, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-03'},
    {'name': 'Gas Bill', 'amount': 40, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-01-02'},
    {'name': 'Groceries', 'amount': 70, 'category': 'food', 'periodicity': 'weekly', 'date': '2024-01-21'},
    {'name': 'Shampoo', 'amount': 10, 'category': 'cosmetics', 'periodicity': 'monthly', 'date': '2024-01-20'},
    {'name': 'Parking Ticket', 'amount': 30, 'category': 'car', 'periodicity': 'one-time', 'date': '2024-01-19'},
    {'name': 'Magazine Subscription', 'amount': 5, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-18'},
    {'name': 'Home Insurance', 'amount': 120, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-01-17'},
    {'name': 'Takeout', 'amount': 25, 'category': 'food', 'periodicity': 'one-time', 'date': '2024-01-16'},
    {'name': 'Face Mask', 'amount': 8, 'category': 'cosmetics', 'periodicity': 'one-time', 'date': '2024-01-15'},
    {'name': 'Car Wash', 'amount': 15, 'category': 'car', 'periodicity': 'monthly', 'date': '2024-01-14'},
    {'name': 'Streaming Service', 'amount': 10, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-13'},
    {'name': 'Property Tax', 'amount': 200, 'category': 'bills and fees', 'periodicity': 'yearly', 'date': '2024-01-12'},
    {'name': 'Lunch', 'amount': 15, 'category': 'food', 'periodicity': 'daily', 'date': '2024-01-11'},
    {'name': 'Face Moisturizer', 'amount': 15, 'category': 'cosmetics', 'periodicity': 'monthly', 'date': '2024-01-10'},
    {'name': 'Car Registration', 'amount': 150, 'category': 'car', 'periodicity': 'yearly', 'date': '2024-01-09'},
    {'name': 'Music Service', 'amount': 10, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-08'},
    {'name': 'Water Bill', 'amount': 30, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-01-07'},
    {'name': 'Dinner', 'amount': 40, 'category': 'food', 'periodicity': 'daily', 'date': '2024-01-06'},
    {'name': 'Body Lotion', 'amount': 12, 'category': 'cosmetics', 'periodicity': 'one-time', 'date': '2024-01-05'},
    {'name': 'Car Insurance', 'amount': 100, 'category': 'car', 'periodicity': 'monthly', 'date': '2024-01-04'},
    {'name': 'Video Streaming', 'amount': 15, 'category': 'subscription', 'periodicity': 'monthly', 'date': '2024-01-03'},
    {'name': 'Electricity Bill', 'amount': 50, 'category': 'bills and fees', 'periodicity': 'monthly', 'date': '2024-01-02'},
]

for expense in expenses_list:
    doc_ref = db.collection('expensesCollection').document()
    batch.set(doc_ref, expense)

batch.commit()