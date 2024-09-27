# events/models.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['bookmyshow_db']

events_collection = db['events']
locations_collection = db['locations']  # Assuming pre-existing locations

class Event:
    def __init__(self, manager_id, title, description, date, time, location_id, available_tickets, payment_options):
        self.manager_id = manager_id
        self.title = title
        self.description = description
        self.date = date
        self.time = time
        self.location_id = location_id
        self.available_tickets = available_tickets
        self.payment_options = payment_options
        self.created_at = datetime.now()

    def save(self):
        # Save event data to the database
        event_data = {
            'manager_id': ObjectId(self.manager_id),
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'location_id': ObjectId(self.location_id),
            'available_tickets': self.available_tickets,
            'payment_options': self.payment_options,
            'created_at': self.created_at
        }
        return events_collection.insert_one(event_data)

    @staticmethod
    def filter_events(location_id=None, date=None, category=None):
        # Create the filter based on available fields
        filter_conditions = {}
        if location_id:
            filter_conditions['location_id'] = ObjectId(location_id)
        if date:
            filter_conditions['date'] = {'$eq': date}
        if category:
            filter_conditions['category'] = category
        
        return list(events_collection.find(filter_conditions))
