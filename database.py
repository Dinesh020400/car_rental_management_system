from pymongo import MongoClient
from config import Config
import json
import os

class MongoDB:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB_NAME]
        
        # Collections
        self.users = self.db.users
        self.cars = self.db.cars
        self.bookings = self.db.bookings
        self.payments = self.db.payments
        self.otps = self.db.otps
        self.reviews = self.db.reviews
        self.notifications = self.db.notifications
        
        # Create indexes
        self.users.create_index('username', unique=True)
        self.users.create_index('email', unique=True)
        self.otps.create_index('created_at', expireAfterSeconds=600)  # OTP expires in 10 minutes
        self.reviews.create_index([('car_id', 1), ('created_at', -1)])
        self.reviews.create_index([('user_id', 1), ('created_at', -1)])
    
    def migrate_from_json(self):
        """Migrate existing JSON data to MongoDB"""
        # Migrate users
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                for user in users_data:
                    # Check if user already exists
                    if not self.users.find_one({'username': user['username']}):
                        # Add default email and phone if not present
                        if 'email' not in user:
                            user['email'] = f"{user['username']}@example.com"
                        if 'phone' not in user:
                            user['phone'] = ''
                        if 'profile_picture' not in user:
                            user['profile_picture'] = ''
                        self.users.insert_one(user)
        
        # Migrate cars
        if os.path.exists('cars.json'):
            with open('cars.json', 'r') as f:
                cars_data = json.load(f)
                for car in cars_data:
                    if not self.cars.find_one({'id': car['id']}):
                        # Add vehicle_type if not present (default to 'car')
                        if 'vehicle_type' not in car:
                            car['vehicle_type'] = 'car'
                        if 'rating' not in car:
                            car['rating'] = 0
                        if 'review_count' not in car:
                            car['review_count'] = 0
                        self.cars.insert_one(car)
        
        # Migrate bookings
        if os.path.exists('bookings.json'):
            with open('bookings.json', 'r') as f:
                bookings_data = json.load(f)
                for booking in bookings_data:
                    if not self.bookings.find_one({'id': booking['id']}):
                        # Add payment_status if not present
                        if 'payment_status' not in booking:
                            booking['payment_status'] = 'pending'
                        if 'payment_method' not in booking:
                            booking['payment_method'] = ''
                        if 'pickup_location' not in booking:
                            booking['pickup_location'] = 'Not specified'
                        if 'drop_location' not in booking:
                            booking['drop_location'] = 'Not specified'
                        if 'pickup_time' not in booking:
                            booking['pickup_time'] = '09:00 AM'
                        if 'drop_time' not in booking:
                            booking['drop_time'] = '09:00 AM'
                        self.bookings.insert_one(booking)
    
    def close(self):
        self.client.close()

# Initialize MongoDB connection
mongodb = MongoDB()
