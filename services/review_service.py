from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import mongodb
from bson import ObjectId

class ReviewService:
    """Service for managing reviews and ratings"""
    
    @staticmethod
    def add_review(user_id, booking_id, car_id, rating, comment, service_rating=None):
        """Add a new review for a completed booking"""
        try:
            # Validate rating
            if not 1 <= rating <= 5:
                return False, "Rating must be between 1 and 5"
            
            # Check if booking exists and is completed
            booking = mongodb.bookings.find_one({'id': booking_id})
            if not booking:
                return False, "Booking not found"
            
            if booking.get('status') != 'completed':
                return False, "Can only review completed bookings"
            
            # Check if review already exists
            existing_review = mongodb.reviews.find_one({
                'booking_id': booking_id,
                'user_id': user_id
            })
            
            if existing_review:
                return False, "You have already reviewed this booking"
            
            # Create review
            review = {
                'id': str(ObjectId()),
                'user_id': user_id,
                'booking_id': booking_id,
                'car_id': car_id,
                'rating': rating,
                'comment': comment,
                'service_rating': service_rating or rating,
                'created_at': datetime.utcnow(),
                'helpful_count': 0,
                'verified_booking': True
            }
            
            mongodb.reviews.insert_one(review)
            
            # Update car's average rating
            ReviewService._update_car_rating(car_id)
            
            return True, "Review added successfully"
        
        except Exception as e:
            print(f"Error adding review: {e}")
            return False, str(e)
    
    @staticmethod
    def _update_car_rating(car_id):
        """Update car's average rating"""
        try:
            # Get all reviews for this car
            reviews = list(mongodb.reviews.find({'car_id': car_id}))
            
            if reviews:
                total_rating = sum(r['rating'] for r in reviews)
                avg_rating = round(total_rating / len(reviews), 1)
                review_count = len(reviews)
                
                mongodb.cars.update_one(
                    {'id': car_id},
                    {'$set': {
                        'rating': avg_rating,
                        'review_count': review_count
                    }}
                )
        except Exception as e:
            print(f"Error updating car rating: {e}")
    
    @staticmethod
    def get_car_reviews(car_id, limit=10, offset=0):
        """Get reviews for a specific car"""
        try:
            reviews = list(mongodb.reviews.find({'car_id': car_id})
                          .sort('created_at', -1)
                          .skip(offset)
                          .limit(limit))
            
            # Enrich with user information
            for review in reviews:
                user = mongodb.users.find_one({'_id': review['user_id']}) or \
                       mongodb.users.find_one({'username': review['user_id']})
                if user:
                    review['user_name'] = user.get('username', 'Anonymous')
                else:
                    review['user_name'] = 'Anonymous'
            
            return reviews
        except Exception as e:
            print(f"Error getting car reviews: {e}")
            return []
    
    @staticmethod
    def get_user_reviews(user_id):
        """Get all reviews by a user"""
        try:
            reviews = list(mongodb.reviews.find({'user_id': user_id})
                          .sort('created_at', -1))
            
            # Enrich with car information
            for review in reviews:
                car = mongodb.cars.find_one({'id': review['car_id']})
                if car:
                    review['car_name'] = car.get('name', 'Unknown')
                    review['car_brand'] = car.get('brand', '')
                else:
                    review['car_name'] = 'Unknown Vehicle'
                    review['car_brand'] = ''
            
            return reviews
        except Exception as e:
            print(f"Error getting user reviews: {e}")
            return []
    
    @staticmethod
    def get_review_stats(car_id):
        """Get review statistics for a car"""
        try:
            reviews = list(mongodb.reviews.find({'car_id': car_id}))
            
            if not reviews:
                return {
                    'average_rating': 0,
                    'total_reviews': 0,
                    'rating_distribution': {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
                }
            
            total_rating = sum(r['rating'] for r in reviews)
            avg_rating = round(total_rating / len(reviews), 1)
            
            # Calculate rating distribution
            rating_dist = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
            for review in reviews:
                rating_dist[review['rating']] += 1
            
            return {
                'average_rating': avg_rating,
                'total_reviews': len(reviews),
                'rating_distribution': rating_dist
            }
        except Exception as e:
            print(f"Error getting review stats: {e}")
            return {
                'average_rating': 0,
                'total_reviews': 0,
                'rating_distribution': {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
            }
    
    @staticmethod
    def mark_review_helpful(review_id, user_id):
        """Mark a review as helpful"""
        try:
            # Check if user already marked this review as helpful
            review = mongodb.reviews.find_one({'id': review_id})
            if not review:
                return False
            
            helpful_users = review.get('helpful_users', [])
            if user_id in helpful_users:
                return False  # Already marked as helpful
            
            # Update helpful count
            mongodb.reviews.update_one(
                {'id': review_id},
                {
                    '$inc': {'helpful_count': 1},
                    '$push': {'helpful_users': user_id}
                }
            )
            return True
        except Exception as e:
            print(f"Error marking review helpful: {e}")
            return False
    
    @staticmethod
    def can_user_review(user_id, booking_id):
        """Check if user can review this booking"""
        try:
            booking = mongodb.bookings.find_one({
                'id': booking_id,
                'user_id': user_id,
                'status': 'completed'
            })
            
            if not booking:
                return False
            
            # Check if already reviewed
            existing_review = mongodb.reviews.find_one({
                'booking_id': booking_id,
                'user_id': user_id
            })
            
            return existing_review is None
        except Exception as e:
            print(f"Error checking review eligibility: {e}")
            return False
