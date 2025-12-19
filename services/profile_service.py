from database import mongodb
from werkzeug.utils import secure_filename
from bson import ObjectId
import os

class ProfileService:
    @staticmethod
    def _get_user_query(user_id):
        """Helper to create user query handling both ObjectId and string IDs"""
        try:
            # Try as ObjectId first
            if isinstance(user_id, str) and len(user_id) == 24:
                return {'_id': ObjectId(user_id)}
        except:
            pass
        # Fall back to direct comparison
        return {'_id': user_id}
    
    @staticmethod
    def get_user_profile(user_id):
        """Get user profile by ID"""
        query = ProfileService._get_user_query(user_id)
        user = mongodb.users.find_one(query)
        if user:
            # Remove password from response
            user.pop('password', None)
            return {'success': True, 'user': user}
        return {'success': False, 'message': 'User not found'}
    
    @staticmethod
    def update_profile(user_id, data, profile_picture=None):
        """Update user profile"""
        query = ProfileService._get_user_query(user_id)
        update_data = {}
        
        # Update basic info
        if 'email' in data and data['email']:
            # Check if email is already used
            existing = mongodb.users.find_one({
                'email': data['email'],
                '_id': {'$ne': query['_id']}
            })
            if existing:
                return {'success': False, 'message': 'Email already in use'}
            update_data['email'] = data['email']
            update_data['email_verified'] = False  # Need to verify new email
        
        if 'phone' in data and data['phone']:
            update_data['phone'] = data['phone']
        
        # Handle profile picture upload
        if profile_picture:
            filename = secure_filename(f"{user_id}_{profile_picture.filename}")
            upload_folder = 'static/profile_pictures'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            filepath = os.path.join(upload_folder, filename)
            profile_picture.save(filepath)
            update_data['profile_picture'] = f'/static/profile_pictures/{filename}'
        
        if update_data:
            mongodb.users.update_one(query, {'$set': update_data})
            return {'success': True, 'message': 'Profile updated successfully'}
        
        return {'success': False, 'message': 'No data to update'}
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password"""
        from auth_service import AuthService
        
        query = ProfileService._get_user_query(user_id)
        user = mongodb.users.find_one(query)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        # Verify old password
        if not AuthService.verify_password(old_password, user['password']):
            return {'success': False, 'message': 'Current password is incorrect'}
        
        # Update password
        hashed_password = AuthService.hash_password(new_password)
        mongodb.users.update_one(
            query,
            {'$set': {'password': hashed_password}}
        )
        
        return {'success': True, 'message': 'Password changed successfully'}
    
    @staticmethod
    def get_user_bookings(user_id):
        """Get all bookings for a user"""
        bookings = list(mongodb.bookings.find({'user_id': str(user_id)}))
        
        # Enrich with car details
        for booking in bookings:
            car = mongodb.cars.find_one({'id': booking['car_id']})
            if car:
                booking['car'] = car
        
        return {'success': True, 'bookings': bookings}
