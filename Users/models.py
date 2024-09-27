# users/models.py
from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    def __init__(self, db_uri='mongodb://localhost:27017/', db_name='bookmyshow_db'):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.users_collection = self.db['users']
        
        # Create unique indexes for email and username
        self.users_collection.create_index("email", unique=True)
        self.users_collection.create_index("username", unique=True)

    def create_user(self, username, email, password, role='USER'):
        hashed_password = generate_password_hash(password)

        if not role in ['USER', 'EVENT_MANAGER']:  # Validate role
            raise ValueError("Invalid role provided.")
        
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': role,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        
        try:
            self.users_collection.insert_one(user_data)
            return user_data
        except Exception as e:
            if "duplicate key error" in str(e):
                raise ValueError("Username or email already exists.")
            else:
                raise Exception("An error occurred while creating the user.")

    def find_user_by_username(self, username):
        return self.users_collection.find_one({'username': username})

    def check_user_password(self, username, password):
        user = self.find_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            return True
        return False

    def update_user_role(self, username, new_role):
        result = self.users_collection.update_one(
            {'username': username},
            {'$set': {'role': new_role, 'updated_at': datetime.now()}}
        )
        if result.matched_count == 0:
            raise ValueError("User not found.")
