# payment/models.py
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['bookmyshow_db']

payments_collection = db['payments']  # Collection to store payment records (optional)

class Payment:
    def __init__(self, booking_id, amount, payment_status):
        self.booking_id = booking_id
        self.amount = amount
        self.payment_status = payment_status  # 'completed', 'reverted'

    def save(self):
        payment_data = {
            'booking_id': ObjectId(self.booking_id),
            'amount': self.amount,
            'payment_status': self.payment_status,
        }
        return payments_collection.insert_one(payment_data)
