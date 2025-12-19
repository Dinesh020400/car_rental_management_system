from datetime import datetime, timedelta
import random
import math

class GPSTracker:
    """GPS tracking simulation for vehicle movement demonstration"""
    
    # Predefined routes with coordinates (Mumbai area for demo)
    ROUTES = {
        'airport_to_city': [
            {'lat': 19.0896, 'lng': 72.8656, 'location': 'Airport Terminal'},
            {'lat': 19.0969, 'lng': 72.8560, 'location': 'Andheri'},
            {'lat': 19.1076, 'lng': 72.8370, 'location': 'Bandra'},
            {'lat': 19.1136, 'lng': 72.8697, 'location': 'Central Mumbai'},
        ],
        'station_to_mall': [
            {'lat': 19.0760, 'lng': 72.8777, 'location': 'New Busstand'},
            {'lat': 19.0740, 'lng': 72.8826, 'location': 'Downtown'},
            {'lat': 19.0930, 'lng': 72.9034, 'location': 'Phoenix Mall'},
        ],
        'city_center_tour': [
            {'lat': 19.1136, 'lng': 72.8697, 'location': 'City Center'},
            {'lat': 19.1176, 'lng': 72.8471, 'location': 'Marine Drive'},
            {'lat': 19.1085, 'lng': 72.8367, 'location': 'Colaba'},
            {'lat': 19.1136, 'lng': 72.8697, 'location': 'Back to Center'},
        ]
    }
    
    @staticmethod
    def get_route(route_name='airport_to_city'):
        """Get a predefined route"""
        return GPSTracker.ROUTES.get(route_name, GPSTracker.ROUTES['airport_to_city'])
    
    @staticmethod
    def generate_route_waypoints(start_lat, start_lng, end_lat, end_lng, num_points=10):
        """Generate intermediate waypoints between two locations"""
        waypoints = []
        
        for i in range(num_points + 1):
            progress = i / num_points
            
            # Linear interpolation with slight randomness for realistic path
            lat = start_lat + (end_lat - start_lat) * progress
            lng = start_lng + (end_lng - start_lng) * progress
            
            # Add small random deviation (within 0.01 degrees ~ 1km)
            lat += random.uniform(-0.005, 0.005)
            lng += random.uniform(-0.005, 0.005)
            
            waypoints.append({
                'lat': round(lat, 6),
                'lng': round(lng, 6),
                'timestamp': datetime.now() + timedelta(minutes=i*5)
            })
        
        return waypoints
    
    @staticmethod
    def calculate_distance(lat1, lng1, lat2, lng2):
        """Calculate distance between two coordinates using Haversine formula (in km)"""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return round(R * c, 2)
    
    @staticmethod
    def get_current_position(booking_id):
        """Simulate getting current GPS position for a booking"""
        # In production, this would fetch from GPS device or database
        # For demo, we'll generate a random position
        
        route = GPSTracker.ROUTES['airport_to_city']
        random_point = random.choice(route)
        
        return {
            'booking_id': booking_id,
            'current_lat': random_point['lat'] + random.uniform(-0.002, 0.002),
            'current_lng': random_point['lng'] + random.uniform(-0.002, 0.002),
            'location': random_point['location'],
            'timestamp': datetime.now().isoformat(),
            'speed': random.randint(20, 60),  # km/h
            'status': 'moving'
        }
    
    @staticmethod
    def simulate_journey(booking_id, route_name='airport_to_city', duration_minutes=30):
        """Simulate a complete journey with GPS tracking"""
        route = GPSTracker.get_route(route_name)
        journey_data = []
        
        total_points = len(route)
        time_per_segment = duration_minutes / total_points
        
        for i, point in enumerate(route):
            journey_data.append({
                'booking_id': booking_id,
                'lat': point['lat'],
                'lng': point['lng'],
                'location': point['location'],
                'timestamp': (datetime.now() + timedelta(minutes=i*time_per_segment)).isoformat(),
                'speed': random.randint(20, 60),
                'progress': round((i / (total_points - 1)) * 100, 1) if total_points > 1 else 100
            })
        
        return journey_data
    
    @staticmethod
    def get_tracking_url(booking_id):
        """Generate a tracking URL for sharing"""
        return f"/track/{booking_id}"
    
    @staticmethod
    def estimate_arrival_time(current_lat, current_lng, dest_lat, dest_lng, avg_speed=40):
        """Estimate arrival time based on distance and speed"""
        distance = GPSTracker.calculate_distance(current_lat, current_lng, dest_lat, dest_lng)
        time_hours = distance / avg_speed
        arrival = datetime.now() + timedelta(hours=time_hours)
        
        return {
            'distance_km': distance,
            'estimated_time_minutes': round(time_hours * 60, 0),
            'estimated_arrival': arrival.strftime('%I:%M %p'),
            'arrival_datetime': arrival.isoformat()
        }
    
    @staticmethod
    def get_geofence_alert(lat, lng, fence_lat, fence_lng, radius_km=1.0):
        """Check if vehicle is within geofence radius"""
        distance = GPSTracker.calculate_distance(lat, lng, fence_lat, fence_lng)
        
        return {
            'within_fence': distance <= radius_km,
            'distance_km': distance,
            'alert': 'Vehicle approaching destination' if distance <= radius_km else 'Vehicle on route'
        }
