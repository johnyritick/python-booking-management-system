# users/services.py
from .models import UserManager  # Adjust the import if your UserManager class is located in a different file
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from .utils import send_email  # Import the send_email function
import jwt
from django.conf import settings

user_manager = UserManager() 

class UserAlreadyExists(Exception):
    pass

class AuthenticationFailed(Exception):
    pass

def register_user(email, name, username, password,role='USER'):
    if role not in ['USER', 'EVENT_MANAGER']:
        raise ValueError("Invalid role provided.")
    # Check if email or username already exists
    if user_manager.users_collection.find_one({'$or': [{'email': email}, {'username': username}] }):
        raise UserAlreadyExists("Email or Username already exists.")
    
    user = user_manager.create_user(username, email, password,role)

    # Send a registration email
    subject = "Welcome to BookMyShow!"
    message = f"Hello {name},\n\nThank you for registering at BookMyShow! Your username is {username}."
    send_email(subject, message, [email])  # Send email notification
    
    return user


def authenticate_user(email, password):
    user = user_manager.users_collection.find_one({'email': email})
    if not user:
        raise AuthenticationFailed("User not found.")
    
    if not check_password_hash(user['password'], password):
        raise AuthenticationFailed("Incorrect password.")
    
    # Generate JWT tokens
    access_token = generate_jwt_token(user, token_type='access')
    refresh_token = generate_jwt_token(user, token_type='refresh')
    
    return {'access_token': access_token, 'refresh_token': refresh_token}

def generate_jwt_token(user, token_type='access'):
    payload = {
        'user_id': str(user['_id']),
        'email': user['email'],
        'role': user.get('role', 'USER'),
        'type': token_type,
        'exp': datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRY if token_type == 'access' else settings.REFRESH_TOKEN_EXPIRY),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token
