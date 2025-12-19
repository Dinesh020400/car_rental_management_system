from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import mongodb

class LocationService:
    """Service for managing pickup/drop locations and time slots"""
    
    # Predefined locations
    LOCATIONS = [
        {'id': 'loc1', 'name': 'Airport Terminal', 'address': 'International Airport, Terminal 1', 'city': 'Mumbai'},
        {'id': 'loc2', 'name': 'Railway Station', 'address': 'Central Railway Station', 'city': 'Mumbai'},
        {'id': 'loc3', 'name': 'City Center', 'address': 'Main Street, Downtown', 'city': 'Mumbai'},
        {'id': 'loc4', 'name': 'Mall Parking', 'address': 'Phoenix Mall, Parking Level 2', 'city': 'Mumbai'},
        {'id': 'loc5', 'name': 'Hotel Grand', 'address': 'Grand Hotel, Lobby', 'city': 'Mumbai'},
        {'id': 'loc6', 'name': 'Bus Terminal', 'address': 'Central Bus Stand', 'city': 'Mumbai'},
    ]
    
    # Time slots (24-hour format)
    TIME_SLOTS = [
        '06:00 AM', '07:00 AM', '08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM',
        '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM', '05:00 PM',
        '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM', '10:00 PM'
    ]
    
    @staticmethod
    def get_all_locations():
        """Get all available pickup/drop locations"""
        return LocationService.LOCATIONS
    
    @staticmethod
    def get_location_by_id(location_id):
        """Get location details by ID"""
        for location in LocationService.LOCATIONS:
            if location['id'] == location_id:
                return location
        return None
    
    @staticmethod
    def get_available_time_slots(date_str):
        """Get available time slots for a given date"""
        # Return all slots if no date provided or invalid date
        if not date_str or date_str.strip() == '':
            return LocationService.TIME_SLOTS
            
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            
            # If selected date is today, filter out past time slots
            if selected_date == current_date:
                available_slots = []
                for slot in LocationService.TIME_SLOTS:
                    slot_time = datetime.strptime(slot, '%I:%M %p').time()
                    if slot_time > current_time:
                        available_slots.append(slot)
                return available_slots if available_slots else LocationService.TIME_SLOTS
            else:
                return LocationService.TIME_SLOTS
        except ValueError:
            # Return all slots if date format is invalid
            return LocationService.TIME_SLOTS
        except Exception as e:
            print(f"Error in get_available_time_slots: {e}")
            return LocationService.TIME_SLOTS
    
    @staticmethod
    def save_pickup_drop_details(booking_id, pickup_location, drop_location, pickup_time, drop_time):
        """Save pickup and drop details for a booking"""
        try:
            mongodb.bookings.update_one(
                {'id': booking_id},
                {'$set': {
                    'pickup_location': pickup_location,
                    'drop_location': drop_location,
                    'pickup_time': pickup_time,
                    'drop_time': drop_time,
                    'updated_at': datetime.utcnow()
                }}
            )
            return True
        except Exception as e:
            print(f"Error saving pickup/drop details: {e}")
            return False
    
    @staticmethod
    def get_booking_location_details(booking_id):
        """Get location details for a booking"""
        try:
            booking = mongodb.bookings.find_one({'id': booking_id})
            if booking:
                return {
                    'pickup_location': booking.get('pickup_location'),
                    'drop_location': booking.get('drop_location'),
                    'pickup_time': booking.get('pickup_time'),
                    'drop_time': booking.get('drop_time')
                }
            return None
        except Exception as e:
            print(f"Error getting location details: {e}")
            return None
    
    @staticmethod
    def calculate_distance_charge(pickup_location_id, drop_location_id):
        """Calculate additional charge based on distance between locations"""
        # Simple distance-based pricing (can be enhanced with actual distance calculation)
        if pickup_location_id == drop_location_id:
            return 0  # Same location, no extra charge
        else:
            return 200  # Different locations, flat extra charge
