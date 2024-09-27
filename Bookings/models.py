# bookings/models.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['bookmyshow_db']

bookings_collection = db['bookings']
events_collection = db['events']
users_collection = db['users']

class Booking:
    def __init__(self, user_id, event_id, tickets):
        self.user_id = user_id
        self.event_id = event_id
        self.tickets = tickets
        self.status = 'active'  # Can be 'active' or 'canceled'
        self.booking_date = datetime.now()

    def save(self):
        # Save the booking to the database
        booking_data = {
            'user_id': ObjectId(self.user_id),
            'event_id': ObjectId(self.event_id),
            'tickets': self.tickets,
            'status': self.status,
            'booking_date': self.booking_date
        }
        return bookings_collection.insert_one(booking_data)

    @staticmethod
    def find_by_user(user_id):
        # Get all bookings by a user
        return list(bookings_collection.find({'user_id': ObjectId(user_id), 'status': 'active'}))

    @staticmethod
    def cancel_booking(booking_id):
        # Cancel the booking
        return bookings_collection.update_one(
            {'_id': ObjectId(booking_id)},
            {'$set': {'status': 'canceled'}}
        )

    @staticmethod
    def find_by_id(booking_id):
        # Find booking by ID
        return bookings_collection.find_one({'_id': ObjectId(booking_id), 'status': 'active'})

    @staticmethod
    def check_event_availability(event_id, tickets):
        # Check if the event has enough available tickets
        event = events_collection.find_one({'_id': ObjectId(event_id)})
        if event and event['available_tickets'] >= tickets:
            return True
        return False

    @staticmethod
    def update_event_tickets(event_id, tickets):
        # Update the available tickets for the event
        return events_collection.update_one(
            {'_id': ObjectId(event_id)},
            {'$inc': {'available_tickets': -tickets}}
        )

    @staticmethod
    def update_booking_status(booking_id, status):
        return bookings_collection.update_one(
            {'_id': ObjectId(booking_id)},
            {'$set': {'status': status}}
        )
