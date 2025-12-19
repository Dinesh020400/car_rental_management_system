from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import mongodb
from collections import defaultdict

class AnalyticsService:
    """Service for admin analytics and reporting"""
    
    @staticmethod
    def get_dashboard_stats():
        """Get overall dashboard statistics"""
        try:
            total_users = mongodb.users.count_documents({})
            total_cars = mongodb.cars.count_documents({})
            total_bookings = mongodb.bookings.count_documents({})
            active_bookings = mongodb.bookings.count_documents({'status': 'active'})
            completed_bookings = mongodb.bookings.count_documents({'status': 'completed'})
            
            # Calculate total revenue
            total_revenue = 0
            payments = mongodb.payments.find({'status': 'completed'})
            for payment in payments:
                total_revenue += payment.get('amount', 0)
            
            # Get today's bookings
            today = datetime.now().date()
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            today_bookings = mongodb.bookings.count_documents({
                'created_at': {'$gte': today_start, '$lte': today_end}
            })
            
            return {
                'total_users': total_users,
                'total_cars': total_cars,
                'total_bookings': total_bookings,
                'active_bookings': active_bookings,
                'completed_bookings': completed_bookings,
                'total_revenue': total_revenue,
                'today_bookings': today_bookings
            }
        except Exception as e:
            print(f"Error getting dashboard stats: {e}")
            return {}
    
    @staticmethod
    def get_revenue_chart_data(days=30):
        """Get revenue data for chart (last N days)"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get payments in date range
            payments = mongodb.payments.find({
                'status': 'completed',
                'created_at': {'$gte': start_date, '$lte': end_date}
            })
            
            # Group by date
            revenue_by_date = defaultdict(float)
            for payment in payments:
                date_key = payment['created_at'].strftime('%Y-%m-%d')
                revenue_by_date[date_key] += payment.get('amount', 0)
            
            # Generate all dates in range
            dates = []
            revenues = []
            current_date = start_date.date()
            
            for i in range(days):
                date_str = current_date.strftime('%Y-%m-%d')
                dates.append(current_date.strftime('%b %d'))
                revenues.append(revenue_by_date.get(date_str, 0))
                current_date += timedelta(days=1)
            
            return {
                'labels': dates,
                'data': revenues
            }
        except Exception as e:
            print(f"Error getting revenue chart data: {e}")
            return {'labels': [], 'data': []}
    
    @staticmethod
    def get_booking_chart_data(days=30):
        """Get booking statistics for chart"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            bookings = mongodb.bookings.find({
                'created_at': {'$gte': start_date, '$lte': end_date}
            })
            
            # Group by date and status
            bookings_by_date = defaultdict(lambda: {'active': 0, 'completed': 0, 'cancelled': 0})
            
            for booking in bookings:
                date_key = booking['created_at'].strftime('%Y-%m-%d') if isinstance(booking['created_at'], datetime) else booking['created_at'][:10]
                status = booking.get('status', 'active')
                bookings_by_date[date_key][status] += 1
            
            # Generate all dates
            dates = []
            active_data = []
            completed_data = []
            cancelled_data = []
            current_date = start_date.date()
            
            for i in range(days):
                date_str = current_date.strftime('%Y-%m-%d')
                dates.append(current_date.strftime('%b %d'))
                data = bookings_by_date.get(date_str, {'active': 0, 'completed': 0, 'cancelled': 0})
                active_data.append(data['active'])
                completed_data.append(data['completed'])
                cancelled_data.append(data['cancelled'])
                current_date += timedelta(days=1)
            
            return {
                'labels': dates,
                'datasets': [
                    {'label': 'Active', 'data': active_data},
                    {'label': 'Completed', 'data': completed_data},
                    {'label': 'Cancelled', 'data': cancelled_data}
                ]
            }
        except Exception as e:
            print(f"Error getting booking chart data: {e}")
            return {'labels': [], 'datasets': []}
    
    @staticmethod
    def get_popular_vehicles(limit=5):
        """Get most popular vehicles by booking count"""
        try:
            bookings = mongodb.bookings.find()
            
            # Count bookings per car
            car_bookings = defaultdict(int)
            for booking in bookings:
                car_bookings[booking['car_id']] += 1
            
            # Sort by booking count
            popular_cars = sorted(car_bookings.items(), key=lambda x: x[1], reverse=True)[:limit]
            
            # Get car details
            result = []
            for car_id, booking_count in popular_cars:
                car = mongodb.cars.find_one({'id': car_id})
                if car:
                    result.append({
                        'car_id': car_id,
                        'name': car.get('name', 'Unknown'),
                        'brand': car.get('brand', ''),
                        'booking_count': booking_count,
                        'revenue': booking_count * car.get('price', 0)
                    })
            
            return result
        except Exception as e:
            print(f"Error getting popular vehicles: {e}")
            return []
    
    @staticmethod
    def get_vehicle_type_distribution():
        """Get distribution of bookings by vehicle type"""
        try:
            cars = mongodb.cars.find()
            bookings = list(mongodb.bookings.find())
            
            # Count bookings by vehicle type
            type_distribution = defaultdict(int)
            
            for booking in bookings:
                car = mongodb.cars.find_one({'id': booking['car_id']})
                if car:
                    vehicle_type = car.get('vehicle_type', 'car')
                    type_distribution[vehicle_type] += 1
            
            return dict(type_distribution)
        except Exception as e:
            print(f"Error getting vehicle type distribution: {e}")
            return {}
    
    @staticmethod
    def get_user_statistics():
        """Get user-related statistics"""
        try:
            total_users = mongodb.users.count_documents({})
            
            # Count users by role
            admin_count = mongodb.users.count_documents({'role': 'admin'})
            customer_count = total_users - admin_count
            
            # Get recent registrations (last 7 days)
            week_ago = datetime.now() - timedelta(days=7)
            recent_registrations = mongodb.users.count_documents({
                'created_at': {'$gte': week_ago}
            })
            
            # Get active users (users with bookings in last 30 days)
            month_ago = datetime.now() - timedelta(days=30)
            recent_bookings = mongodb.bookings.find({
                'created_at': {'$gte': month_ago}
            })
            
            active_users = set()
            for booking in recent_bookings:
                active_users.add(booking['user_id'])
            
            return {
                'total_users': total_users,
                'admin_count': admin_count,
                'customer_count': customer_count,
                'recent_registrations': recent_registrations,
                'active_users': len(active_users)
            }
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return {}
    
    @staticmethod
    def get_payment_method_stats():
        """Get statistics by payment method"""
        try:
            payments = mongodb.payments.find({'status': 'completed'})
            
            method_stats = defaultdict(lambda: {'count': 0, 'amount': 0})
            
            for payment in payments:
                method = payment.get('payment_method', 'unknown')
                method_stats[method]['count'] += 1
                method_stats[method]['amount'] += payment.get('amount', 0)
            
            return dict(method_stats)
        except Exception as e:
            print(f"Error getting payment method stats: {e}")
            return {}
    
    @staticmethod
    def generate_monthly_report(year, month):
        """Generate comprehensive monthly report"""
        try:
            # Get month date range
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
            
            # Get bookings in month
            bookings = list(mongodb.bookings.find({
                'created_at': {'$gte': start_date, '$lte': end_date}
            }))
            
            # Get payments in month
            payments = list(mongodb.payments.find({
                'created_at': {'$gte': start_date, '$lte': end_date},
                'status': 'completed'
            }))
            
            total_revenue = sum(p.get('amount', 0) for p in payments)
            total_bookings = len(bookings)
            completed_bookings = len([b for b in bookings if b.get('status') == 'completed'])
            cancelled_bookings = len([b for b in bookings if b.get('status') == 'cancelled'])
            
            return {
                'month': start_date.strftime('%B %Y'),
                'total_bookings': total_bookings,
                'completed_bookings': completed_bookings,
                'cancelled_bookings': cancelled_bookings,
                'total_revenue': total_revenue,
                'average_booking_value': total_revenue / total_bookings if total_bookings > 0 else 0
            }
        except Exception as e:
            print(f"Error generating monthly report: {e}")
            return {}
