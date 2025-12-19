import bcrypt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import mongodb

class AuthService:
    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed_password):
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def register_user(username, email, password, phone=''):
        """Register a new user with hashed password"""
        # Check if username or email already exists
        if mongodb.users.find_one({'username': username}):
            return {'success': False, 'message': 'Username already exists'}
        
        if mongodb.users.find_one({'email': email}):
            return {'success': False, 'message': 'Email already exists'}
        
        # Hash password
        hashed_password = AuthService.hash_password(password)
        
        # Create user document
        user = {
            'username': username,
            'email': email,
            'phone': phone,
            'password': hashed_password,
            'is_admin': False,
            'email_verified': False,
            'profile_picture': ''
        }
        
        # Insert user
        result = mongodb.users.insert_one(user)
        user['id'] = str(result.inserted_id)
        
        return {'success': True, 'message': 'User registered successfully', 'user': user}
    
    @staticmethod
    def login_user(username, password):
        """Login user with password verification"""
        user = mongodb.users.find_one({'username': username})
        
        if not user:
            return {'success': False, 'message': 'Invalid username or password'}
        
        # Verify password
        if AuthService.verify_password(password, user['password']):
            return {'success': True, 'message': 'Login successful', 'user': user}
        else:
            return {'success': False, 'message': 'Invalid username or password'}
    
    @staticmethod
    def update_user_profile(user_id, data):
        """Update user profile information"""
        update_data = {}
        
        if 'email' in data:
            # Check if email is already used by another user
            existing = mongodb.users.find_one({'email': data['email'], '_id': {'$ne': user_id}})
            if existing:
                return {'success': False, 'message': 'Email already in use'}
            update_data['email'] = data['email']
        
        if 'phone' in data:
            update_data['phone'] = data['phone']
        
        if 'profile_picture' in data:
            update_data['profile_picture'] = data['profile_picture']
        
        if 'password' in data and data['password']:
            update_data['password'] = AuthService.hash_password(data['password'])
        
        if update_data:
            mongodb.users.update_one({'_id': user_id}, {'$set': update_data})
            return {'success': True, 'message': 'Profile updated successfully'}
        
        return {'success': False, 'message': 'No data to update'}
