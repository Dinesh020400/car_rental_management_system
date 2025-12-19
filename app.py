from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_mail import Mail
from config import Config
from database import mongodb
from services.auth_service import AuthService
from services.email_service import EmailService
from services.profile_service import ProfileService
from services.payment_service import PaymentService
from services.invoice_service_pro import ProfessionalInvoiceGenerator
from services.enhanced_notification import EnhancedNotificationService
from services.location_service import LocationService
from services.review_service import ReviewService
from services.analytics_service import AnalyticsService
from services.gps_tracker import GPSTracker
from datetime import datetime
import uuid
import os
from werkzeug.utils import secure_filename
from bson import ObjectId

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
mail = Mail(app)
email_service = EmailService(app)
invoice_generator = ProfessionalInvoiceGenerator()

# Upload configuration
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# USD to INR conversion rate
USD_TO_INR_RATE = 83.0

def get_car_image(make, model):
    filename = f"{make.lower()}_{model.lower().replace(' ', '_')}_2022.jpg"
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(image_path):
        return f'/static/car_images/{filename}'
    return '/static/car_images/default_car.jpg'

def safe_object_id(id_string):
    """Safely convert string to ObjectId, handling both ObjectId strings and regular strings"""
    try:
        # If it's already a valid 24-char hex string, convert it
        if isinstance(id_string, str) and len(id_string) == 24:
            return ObjectId(id_string)
        # Otherwise return the string as-is for old-style IDs
        return id_string
    except:
        return id_string

def check_and_release_expired_bookings():
    """Check for bookings that have passed their end date and mark vehicles as available"""
    try:
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Find all confirmed bookings that have passed their end date
        expired_bookings = mongodb.bookings.find({
            'status': 'confirmed',
            'end_date': {'$lt': current_date}
        })
        
        for booking in expired_bookings:
            # Update booking status to completed
            mongodb.bookings.update_one(
                {'id': booking['id']},
                {'$set': {'status': 'completed'}}
            )
            
            # Make the car available again
            mongodb.cars.update_one(
                {'id': booking['car_id']},
                {'$set': {'available': True}}
            )
            print(f"Released vehicle {booking['car_id']} from expired booking {booking['id']}")
    except Exception as e:
        print(f"Error checking expired bookings: {e}")

# ==================== HOME & CAR LISTING ====================

@app.route('/')
def index():
    # Check and release expired bookings
    check_and_release_expired_bookings()
    
    search_query = request.args.get('search', '').lower()
    sort_by = request.args.get('sort', 'price_asc')
    make_filter = request.args.get('make', '')
    vehicle_type = request.args.get('type', '')  # Filter by vehicle type

    # Get all cars from MongoDB
    query = {}
    if search_query:
        query = {
            '$or': [
                {'make': {'$regex': search_query, '$options': 'i'}},
                {'model': {'$regex': search_query, '$options': 'i'}},
                {'year': {'$regex': search_query, '$options': 'i'}}
            ]
        }
    
    if make_filter:
        query['make'] = make_filter
    
    if vehicle_type:
        query['vehicle_type'] = vehicle_type
    
    cars = list(mongodb.cars.find(query))
    
    # Convert prices to INR and add default image if missing
    for car in cars:
        car['price_inr'] = round(car.get('price_per_day', 0), 2)
        car['_id'] = str(car.get('_id', ''))
        # Ensure image field exists
        if not car.get('image'):
            car['image'] = get_car_image(car.get('make', ''), car.get('model', ''))
    
    # Sorting
    if sort_by == 'price_asc':
        cars = sorted(cars, key=lambda x: x.get('price_per_day', 0))
    elif sort_by == 'price_desc':
        cars = sorted(cars, key=lambda x: x.get('price_per_day', 0), reverse=True)
    elif sort_by == 'year_desc':
        cars = sorted(cars, key=lambda x: x.get('year', 0), reverse=True)
    elif sort_by == 'year_asc':
        cars = sorted(cars, key=lambda x: x.get('year', 0))
    
    return render_template('index.html', cars=cars)

@app.route('/car/<car_id>')
def car_details(car_id):
    # Try to find by MongoDB _id first, then by custom id field
    car = mongodb.cars.find_one({'_id': safe_object_id(car_id)}) or mongodb.cars.find_one({'id': car_id})
    if car:
        car['price_inr'] = round(car.get('price_per_day', 0), 2)
        car['_id'] = str(car.get('_id', ''))
        # Ensure image field exists
        if not car.get('image'):
            car['image'] = get_car_image(car.get('make', ''), car.get('model', ''))
        
        # Get reviews for this car
        reviews = ReviewService.get_car_reviews(car_id, limit=10)
        review_stats = ReviewService.get_review_stats(car_id)
        
        # Find similar cars
        similar_cars = []
        for other_car in mongodb.cars.find({'id': {'$ne': car_id}, 'available': True}).limit(3):
            if (other_car['make'] == car['make'] or
                (other_car.get('price_per_day', 0) >= car.get('price_per_day', 0) * 0.8 and
                 other_car.get('price_per_day', 0) <= car.get('price_per_day', 0) * 1.2)):
                other_car['price_inr'] = round(other_car.get('price_per_day', 0), 2)
                other_car['_id'] = str(other_car.get('_id', ''))
                similar_cars.append(other_car)
        
        return render_template('car_details.html', car=car, similar_cars=similar_cars, 
                             reviews=reviews, review_stats=review_stats)
    
    flash('Car not found')
    return redirect(url_for('index'))

# ==================== AUTHENTICATION ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        password = request.form.get('password')
        
        result = AuthService.register_user(username, email, password, phone)
        
        if result['success']:
            flash('Registration successful! Please verify your email.')
            # Send verification OTP
            email_service.send_otp(email, username)
            return redirect(url_for('verify_email', email=email))
        else:
            flash(result['message'])
    
    return render_template('register.html')

@app.route('/verify-email')
def verify_email():
    email = request.args.get('email')
    return render_template('verify_email.html', email=email)

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    email = request.form.get('email')
    otp = request.form.get('otp')
    
    result = email_service.verify_otp(email, otp)
    
    if result['success']:
        flash('Email verified successfully! You can now login.')
        return redirect(url_for('login'))
    else:
        flash(result['message'])
        return redirect(url_for('verify_email', email=email))

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    email = request.form.get('email')
    user = mongodb.users.find_one({'email': email})
    
    if user:
        result = email_service.send_otp(email, user['username'])
        if result['success']:
            flash('OTP resent successfully!')
        else:
            flash(result['message'])
    else:
        flash('User not found')
    
    return redirect(url_for('verify_email', email=email))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        result = AuthService.login_user(username, password)
        
        if result['success']:
            user = result['user']
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', False)
            session['email'] = user.get('email', '')
            
            flash('Login successful!')
            # Redirect admin to admin dashboard, regular users to home
            if user.get('is_admin', False):
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash(result['message'])
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('index'))

# ==================== USER PROFILE ====================

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please login to view your profile')
        return redirect(url_for('login'))
    
    result = ProfileService.get_user_profile(safe_object_id(session['user_id']))
    
    if result['success']:
        user = result['user']
        user['_id'] = str(user['_id'])
        return render_template('profile.html', user=user)
    
    flash('Error loading profile')
    return redirect(url_for('index'))

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please login to edit your profile')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            'email': request.form.get('email'),
            'phone': request.form.get('phone')
        }
        
        profile_picture = request.files.get('profile_picture')
        
        result = ProfileService.update_profile(
            safe_object_id(session['user_id']),
            data,
            profile_picture
        )
        
        if result['success']:
            flash(result['message'])
            # Update session email
            session['email'] = data['email']
            return redirect(url_for('profile'))
        else:
            flash(result['message'])
    
    result = ProfileService.get_user_profile(safe_object_id(session['user_id']))
    if result['success']:
        user = result['user']
        user['_id'] = str(user.get('_id', ''))
        return render_template('edit_profile.html', user=user)
    
    flash('Error loading profile')
    return redirect(url_for('profile'))

@app.route('/profile/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    
    result = ProfileService.change_password(
        safe_object_id(session['user_id']),
        old_password,
        new_password
    )
    
    if result['success']:
        flash(result['message'])
    else:
        flash(result['message'])
    
    return redirect(url_for('profile'))

# ==================== BOOKING & PAYMENT ====================

@app.route('/book/<car_id>', methods=['GET', 'POST'])
def book_car(car_id):
    if 'user_id' not in session:
        flash('Please login to book a car')
        return redirect(url_for('login'))
    
    # Prevent admin from booking
    if session.get('is_admin'):
        flash('Admin users cannot book vehicles. Please use a regular user account.')
        return redirect(url_for('car_details', car_id=car_id))
    
    # Try to find by MongoDB _id first, then by custom id field
    car = mongodb.cars.find_one({'_id': safe_object_id(car_id)}) or mongodb.cars.find_one({'id': car_id})
    if not car:
        flash('Car not found')
        return redirect(url_for('index'))
    
    if not car.get('available', False):
        flash('Car is not available for booking')
        return redirect(url_for('car_details', car_id=car_id))
    
    car['price_inr'] = round(car.get('price_per_day', 0), 2)
    car['_id'] = str(car.get('_id', ''))
    
    # Get locations and time slots
    locations = LocationService.get_all_locations()
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        pickup_location = request.form.get('pickup_location')
        drop_location = request.form.get('drop_location')
        pickup_time = request.form.get('pickup_time')
        drop_time = request.form.get('drop_time')
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        duration = end - start
        
        if duration.days < 0:
            flash('End date must be after start date')
            return render_template('book_car.html', car=car, today=datetime.now().strftime('%Y-%m-%d'), 
                                 locations=locations)
        
        total_days = duration.days + 1
        base_price = total_days * car.get('price_per_day', 0)
        
        # Add location charge if different pickup/drop locations
        location_charge = LocationService.calculate_distance_charge(pickup_location, drop_location)
        total_price = base_price + location_charge
        
        # Create booking
        booking = {
            'id': str(uuid.uuid4()),
            'car_id': car_id,
            'user_id': session['user_id'],
            'start_date': start_date,
            'end_date': end_date,
            'total_days': total_days,
            'total_price': total_price,
            'status': 'pending',
            'payment_status': 'pending',
            'payment_method': '',
            'pickup_location': pickup_location,
            'drop_location': drop_location,
            'pickup_time': pickup_time,
            'drop_time': drop_time,
            'created_at': datetime.utcnow()
        }
        
        mongodb.bookings.insert_one(booking)
        
        # Update car availability
        mongodb.cars.update_one({'id': car_id}, {'$set': {'available': False}})
        
        flash('Booking created! Please proceed with payment.')
        return redirect(url_for('payment', booking_id=booking['id']))
    
    return render_template('book_car.html', car=car, today=datetime.now().strftime('%Y-%m-%d'),
                         locations=locations)

@app.route('/payment/<booking_id>')
def payment(booking_id):
    if 'user_id' not in session:
        flash('Please login to proceed with payment')
        return redirect(url_for('login'))
    
    booking = mongodb.bookings.find_one({'id': booking_id, 'user_id': session['user_id']})
    
    if not booking:
        flash('Booking not found')
        return redirect(url_for('my_bookings'))
    
    if booking.get('payment_status') == 'paid':
        flash('This booking is already paid')
        return redirect(url_for('my_bookings'))
    
    # Try to find car by both id and _id
    car = mongodb.cars.find_one({'id': booking['car_id']})
    if not car:
        car = mongodb.cars.find_one({'_id': safe_object_id(booking['car_id'])})
    
    if car:
        # Ensure image field exists
        if not car.get('image'):
            car['image'] = get_car_image(car.get('make', ''), car.get('model', ''))
    
    booking['car'] = car
    booking['_id'] = str(booking.get('_id', ''))
    
    payment_methods = PaymentService.PAYMENT_METHODS
    
    return render_template('payment.html', booking=booking, payment_methods=payment_methods)

@app.route('/process-payment/<booking_id>', methods=['POST'])
def process_payment(booking_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    booking = mongodb.bookings.find_one({'id': booking_id, 'user_id': session['user_id']})
    
    if not booking:
        return jsonify({'success': False, 'message': 'Booking not found'})
    
    payment_method = request.form.get('payment_method')
    
    # Initiate payment
    payment_result = PaymentService.initiate_payment(
        booking_id,
        booking['total_price'],
        payment_method,
        session['user_id']
    )
    
    if not payment_result['success']:
        return jsonify(payment_result)
    
    # Simulate payment processing (in real app, this would be callback from gateway)
    payment_id = payment_result['payment']['id']
    process_result = PaymentService.process_payment(payment_id, {})
    
    if process_result['success']:
        # Update booking status
        mongodb.bookings.update_one(
            {'id': booking_id},
            {'$set': {'status': 'confirmed', 'payment_status': 'paid'}}
        )
        
        # Get required data - try both _id and id field for car lookup
        car = mongodb.cars.find_one({'id': booking['car_id']})
        if not car:
            car = mongodb.cars.find_one({'_id': safe_object_id(booking['car_id'])})
        
        user = mongodb.users.find_one({'_id': safe_object_id(session['user_id'])})
        payment = mongodb.payments.find_one({'id': payment_id})
        
        # Get location names from IDs
        from services.location_service import LocationService
        pickup_loc_id = booking.get('pickup_location', '')
        drop_loc_id = booking.get('drop_location', '')
        pickup_loc = LocationService.get_location_by_id(pickup_loc_id)
        drop_loc = LocationService.get_location_by_id(drop_loc_id)
        
        pickup_location_name = f"{pickup_loc['name']} - {pickup_loc['address']}" if pickup_loc else pickup_loc_id or 'Not specified'
        drop_location_name = f"{drop_loc['name']} - {drop_loc['address']}" if drop_loc else drop_loc_id or 'Not specified'
        
        # Prepare booking data with car details (with None checks)
        booking_data = {
            'id': booking['id'],
            'car_brand': car.get('make', '') if car else 'Unknown',
            'car_model': car.get('model', '') if car else 'Unknown',
            'start_date': booking['start_date'],
            'end_date': booking['end_date'],
            'total_days': booking.get('total_days', 0),
            'total_price': booking['total_price'],
            'pickup_location': pickup_location_name,
            'drop_location': drop_location_name,
            'pickup_time': booking.get('pickup_time', 'N/A'),
            'drop_time': booking.get('drop_time', 'N/A')
        }
        
        payment_data = {
            'method': payment.get('method', 'N/A'),
            'transaction_id': payment.get('transaction_id', 'N/A'),
            'status': 'completed'
        }
        
        user_data = {
            'username': user.get('username', 'Customer'),
            'email': user.get('email', session.get('email', '')),
            'phone': user.get('phone', 'N/A')
        }
        
        # Generate and send combined invoice email
        try:
            success, invoice_info = EnhancedNotificationService.generate_and_send_invoice(
                booking_data, payment_data, user_data
            )
            if not success:
                print("Warning: Invoice generation or email failed")
        except Exception as e:
            print(f"Email/Invoice error: {e}")
        
        flash('Payment successful! Booking confirmed. Check your email for invoice.')
        return jsonify({
            'success': True,
            'redirect': url_for('booking_success', booking_id=booking_id)
        })
    
    return jsonify(process_result)

@app.route('/booking-success/<booking_id>')
def booking_success(booking_id):
    if 'user_id' not in session:
        flash('Please login')
        return redirect(url_for('login'))
    
    booking = mongodb.bookings.find_one({'id': booking_id, 'user_id': session['user_id']})
    
    if not booking:
        flash('Booking not found')
        return redirect(url_for('my_bookings'))
    
    # Try both id and _id field for car lookup
    car = mongodb.cars.find_one({'id': booking['car_id']})
    if not car:
        car = mongodb.cars.find_one({'_id': safe_object_id(booking['car_id'])})
    
    # Provide default values if car not found
    if not car:
        car = {
            'make': 'Unknown',
            'model': 'Vehicle',
            'year': 'N/A',
            'image': '/static/car_images/default_car.jpg'
        }
    
    booking['car'] = car
    booking['_id'] = str(booking.get('_id', ''))
    
    payment = mongodb.payments.find_one({'booking_id': booking_id})
    
    # Get locations for display
    from services.location_service import LocationService
    locations = LocationService.get_all_locations()
    
    return render_template('booking_success.html', booking=booking, payment=payment, locations=locations)

@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        flash('Please login to view your bookings')
        return redirect(url_for('login'))
    
    # Check and release expired bookings
    check_and_release_expired_bookings()
    
    bookings = list(mongodb.bookings.find({'user_id': session['user_id']}))
    
    for booking in bookings:
        # Try both id and _id field for car lookup
        car = mongodb.cars.find_one({'id': booking['car_id']})
        if not car:
            car = mongodb.cars.find_one({'_id': safe_object_id(booking['car_id'])})
        booking['car'] = car
        # Get actual user data for this booking
        user = mongodb.users.find_one({'_id': safe_object_id(booking['user_id'])})
        booking['user'] = {
            'username': user.get('username', 'Unknown') if user else 'Unknown',
            'email': user.get('email', '') if user else ''
        }
        booking['_id'] = str(booking.get('_id', ''))
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/download-invoice/<booking_id>')
def download_invoice(booking_id):
    if 'user_id' not in session:
        flash('Please login')
        return redirect(url_for('login'))
    
    booking = mongodb.bookings.find_one({'id': booking_id, 'user_id': session['user_id']})
    
    if not booking:
        flash('Booking not found')
        return redirect(url_for('my_bookings'))
    
    invoice_id = f"INV-{booking_id[:8].upper()}"
    invoice_path = f"static/invoices/{invoice_id}.pdf"
    
    if os.path.exists(invoice_path):
        return send_file(invoice_path, as_attachment=True, download_name=f"{invoice_id}.pdf")
    
    flash('Invoice not found')
    return redirect(url_for('my_bookings'))

@app.route('/cancel-booking/<booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        flash('Please login')
        return redirect(url_for('login'))
    
    # Check and release expired bookings first
    check_and_release_expired_bookings()
    
    booking = mongodb.bookings.find_one({'id': booking_id, 'user_id': session['user_id']})
    
    if not booking:
        flash('Booking not found')
        return redirect(url_for('my_bookings'))
    
    # Update booking status
    mongodb.bookings.update_one(
        {'id': booking_id},
        {'$set': {'status': 'cancelled'}}
    )
    
    # Make car available
    mongodb.cars.update_one(
        {'id': booking['car_id']},
        {'$set': {'available': True}}
    )
    
    # Process refund if payment was made
    if booking.get('payment_status') == 'paid':
        payment = mongodb.payments.find_one({'booking_id': booking_id})
        if payment:
            PaymentService.refund_payment(payment['id'], 'Booking cancelled by user')
    
    flash('Booking cancelled successfully')
    return redirect(url_for('my_bookings'))

# ==================== ADMIN ROUTES ====================

def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'warning')
            return redirect(url_for('login'))
        if not session.get('is_admin', False):
            flash('Admin access required. You do not have permission to access this area.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin_dashboard():
    # Check and release expired bookings
    check_and_release_expired_bookings()
    
    cars = list(mongodb.cars.find())
    users = list(mongodb.users.find())
    bookings = list(mongodb.bookings.find())
    
    # Attach car details to each booking for display
    for booking in bookings:
        # Try both id and _id field for car lookup
        car = mongodb.cars.find_one({'id': booking['car_id']})
        if not car:
            car = mongodb.cars.find_one({'_id': safe_object_id(booking['car_id'])})
        booking['car'] = car
    
    # Sort bookings by created_at, handling both datetime and string
    def get_created_at(booking):
        created = booking.get('created_at')
        if isinstance(created, str):
            try:
                return datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
            except:
                return datetime.min
        elif isinstance(created, datetime):
            return created
        else:
            return datetime.min
    
    bookings.sort(key=get_created_at, reverse=True)
    
    # Get quick stats
    stats = AnalyticsService.get_dashboard_stats()
    
    return render_template('admin/dashboard.html', cars=cars, users=users, bookings=bookings, stats=stats)

@app.route('/admin/cars')
@admin_required
def admin_cars():
    cars = list(mongodb.cars.find())
    return render_template('admin/cars.html', cars=cars)

@app.route('/admin/add-car', methods=['GET', 'POST'])
@admin_required
def admin_add_car():
    
    if request.method == 'POST':
        car_image = request.files.get('car_image')
        image_url = f"https://via.placeholder.com/150?text={request.form['make']}+{request.form['model']}"
        
        if car_image and allowed_file(car_image.filename):
            filename = secure_filename(f"{uuid.uuid4()}_{car_image.filename}")
            car_image.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = url_for('static', filename=f'car_images/{filename}')
        
        # Generate sequential ID
        last_car = mongodb.cars.find_one(sort=[('id', -1)])
        if last_car and last_car.get('id', '').isdigit():
            next_id = str(int(last_car['id']) + 1)
        else:
            # Find highest numeric ID
            cars = list(mongodb.cars.find())
            numeric_ids = [int(c['id']) for c in cars if c.get('id', '').isdigit()]
            next_id = str(max(numeric_ids) + 1) if numeric_ids else '1'
        
        new_car = {
            'id': next_id,
            'make': request.form.get('make'),
            'model': request.form.get('model'),
            'year': int(request.form.get('year')),
            'price_per_day': float(request.form.get('price_per_day')),
            'vehicle_type': request.form.get('vehicle_type', 'car'),
            'available': True,
            'image': image_url,
            'rating': 0,
            'review_count': 0
        }
        
        mongodb.cars.insert_one(new_car)
        flash('Vehicle added successfully')
        return redirect(url_for('admin_cars'))
    
    return render_template('admin/add_car.html')

@app.route('/admin/edit-car/<car_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_car(car_id):
    
    car = mongodb.cars.find_one({'id': car_id})
    if not car:
        flash('Car not found')
        return redirect(url_for('admin_cars'))
    
    if request.method == 'POST':
        update_data = {
            'make': request.form.get('make'),
            'model': request.form.get('model'),
            'year': int(request.form.get('year')),
            'price_per_day': float(request.form.get('price_per_day')),
            'vehicle_type': request.form.get('vehicle_type', 'car'),
            'available': 'available' in request.form
        }
        
        if request.form.get('image'):
            update_data['image'] = request.form.get('image')
        
        mongodb.cars.update_one({'id': car_id}, {'$set': update_data})
        flash('Car updated successfully')
        return redirect(url_for('admin_cars'))
    
    car['_id'] = str(car.get('_id', ''))
    return render_template('admin/edit_car.html', car=car)

@app.route('/admin/delete-car/<car_id>')
@admin_required
def admin_delete_car(car_id):
    
    mongodb.cars.delete_one({'id': car_id})
    flash('Car deleted successfully')
    return redirect(url_for('admin_cars'))

@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    
    bookings = list(mongodb.bookings.find())
    
    # Sort by created_at descending (latest first)
    def get_sort_key(b):
        created = b.get('created_at')
        if isinstance(created, str):
            try:
                return datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
            except:
                return datetime.min
        return created or datetime.min
        
    bookings.sort(key=get_sort_key, reverse=True)
    
    for booking in bookings:
        # Try both id and _id field for car lookup
        car = mongodb.cars.find_one({'id': booking['car_id']})
        if not car:
            car = mongodb.cars.find_one({'_id': safe_object_id(booking['car_id'])})
        user = mongodb.users.find_one({'_id': safe_object_id(booking['user_id'])})
        booking['car'] = car if car else {'make': 'Unknown', 'model': 'Vehicle', 'year': 'N/A', 'image': '/static/car_images/default_car.jpg', 'id': booking['car_id']}
        booking['user'] = user if user else {'username': 'Unknown User'}
        booking['_id'] = str(booking.get('_id', ''))
    
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/update-booking/<booking_id>', methods=['POST'])
@admin_required
def admin_update_booking(booking_id):
    
    booking = mongodb.bookings.find_one({'id': booking_id})
    if not booking:
        flash('Booking not found')
        return redirect(url_for('admin_bookings'))
    
    status = request.form.get('status')
    mongodb.bookings.update_one({'id': booking_id}, {'$set': {'status': status}})
    
    if status == 'cancelled':
        mongodb.cars.update_one(
            {'id': booking['car_id']},
            {'$set': {'available': True}}
        )
    
    flash('Booking status updated successfully')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/users')
@admin_required
def admin_users():
    
    users = list(mongodb.users.find())
    for user in users:
        user['_id'] = str(user.get('_id', ''))
        user.pop('password', None)  # Remove password from display
    
    return render_template('admin/users.html', users=users)

# ==================== DATA MIGRATION ====================

@app.route('/admin/migrate-data')
@admin_required
def migrate_data():
    
    try:
        mongodb.migrate_from_json()
        flash('Data migrated successfully from JSON to MongoDB!')
    except Exception as e:
        flash(f'Error migrating data: {str(e)}')
    
    return redirect(url_for('admin_dashboard'))

# ==================== FAVICON ====================

@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon') if os.path.exists('static/favicon.ico') else ('', 204)

# ==================== REVIEW ROUTES ====================

@app.route('/add_review/<booking_id>', methods=['GET', 'POST'])
def add_review(booking_id):
    if 'user_id' not in session:
        flash('Please login to add a review')
        return redirect(url_for('login'))
    
    booking = mongodb.bookings.find_one({'id': booking_id, 'user_id': session['user_id']})
    if not booking:
        flash('Booking not found')
        return redirect(url_for('my_bookings'))
    
    if booking.get('status') != 'completed':
        flash('Can only review completed bookings')
        return redirect(url_for('my_bookings'))
    
    car = mongodb.cars.find_one({'id': booking['car_id']})
    
    if request.method == 'POST':
        rating = int(request.form.get('rating', 0))
        service_rating = int(request.form.get('service_rating', 0))
        comment = request.form.get('comment', '')
        
        success, message = ReviewService.add_review(
            session['user_id'],
            booking_id,
            booking['car_id'],
            rating,
            comment,
            service_rating
        )
        
        flash(message)
        if success:
            return redirect(url_for('car_details', car_id=booking['car_id']))
        
    return render_template('add_review.html', booking=booking, car=car)

@app.route('/my_reviews')
def my_reviews():
    if 'user_id' not in session:
        flash('Please login to view your reviews')
        return redirect(url_for('login'))
    
    reviews = ReviewService.get_user_reviews(session['user_id'])
    return render_template('my_reviews.html', reviews=reviews)

# ==================== ANALYTICS ROUTES ====================

@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    stats = AnalyticsService.get_dashboard_stats()
    revenue_data = AnalyticsService.get_revenue_chart_data(days=30)
    booking_data = AnalyticsService.get_booking_chart_data(days=30)
    popular_vehicles = AnalyticsService.get_popular_vehicles(limit=5)
    user_stats = AnalyticsService.get_user_statistics()
    payment_stats = AnalyticsService.get_payment_method_stats()
    vehicle_distribution = AnalyticsService.get_vehicle_type_distribution()
    
    return render_template('admin/analytics.html',
                         stats=stats,
                         revenue_data=revenue_data,
                         booking_data=booking_data,
                         popular_vehicles=popular_vehicles,
                         user_stats=user_stats,
                         payment_stats=payment_stats,
                         vehicle_distribution=vehicle_distribution)

# ==================== API ENDPOINTS ====================

@app.route('/api/time-slots')
def api_time_slots():
    """API endpoint to get available time slots for a date"""
    date_str = request.args.get('date', '')
    time_slots = LocationService.get_available_time_slots(date_str)
    return jsonify({'time_slots': time_slots})

@app.route('/api/locations')
def api_locations():
    """API endpoint to get all locations"""
    locations = LocationService.get_all_locations()
    return jsonify({'locations': locations})

@app.route('/api/vehicle-stats')
@admin_required
def api_vehicle_stats():
    """API endpoint for vehicle statistics"""
    vehicle_type = request.args.get('type', '')
    stats = {
        'total': mongodb.cars.count_documents({'vehicle_type': vehicle_type} if vehicle_type else {}),
        'available': mongodb.cars.count_documents({'vehicle_type': vehicle_type, 'available': True} if vehicle_type else {'available': True}),
        'booked': mongodb.cars.count_documents({'vehicle_type': vehicle_type, 'available': False} if vehicle_type else {'available': False})
    }
    return jsonify(stats)

# ==================== GPS TRACKING ROUTES ====================

@app.route('/track/<booking_id>')
def track_vehicle(booking_id):
    """GPS tracking page for a booking"""
    booking = mongodb.bookings.find_one({'id': booking_id})
    
    if not booking:
        flash('Booking not found')
        return redirect(url_for('index'))
    
    # Get car details with dual lookup
    car = mongodb.cars.find_one({'id': booking['car_id']})
    if not car:
        car = mongodb.cars.find_one({'_id': safe_object_id(booking['car_id'])})
    
    # Prepare booking data for template
    tracking_data = {
        'id': booking['id'],
        'car_brand': car.get('make', 'Vehicle') if car else 'Unknown',
        'car_model': car.get('model', '') if car else 'Vehicle',
        'start_date': booking.get('start_date', 'N/A'),
        'end_date': booking.get('end_date', 'N/A'),
        'pickup_location': booking.get('pickup_location', 'Pickup Location'),
        'drop_location': booking.get('drop_location', 'Drop Location'),
        'pickup_time': booking.get('pickup_time', 'N/A'),
        'drop_time': booking.get('drop_time', 'N/A'),
        'status': booking.get('status', 'active')
    }
    
    return render_template('track_vehicle.html', booking=tracking_data)

@app.route('/api/gps/<booking_id>')
def api_gps_position(booking_id):
    """API endpoint to get current GPS position"""
    position = GPSTracker.get_current_position(booking_id)
    return jsonify(position)

@app.route('/api/gps/journey/<booking_id>')
def api_gps_journey(booking_id):
    """API endpoint to get complete journey simulation"""
    route_name = request.args.get('route', 'airport_to_city')
    journey = GPSTracker.simulate_journey(booking_id, route_name)
    return jsonify({
        'booking_id': booking_id,
        'journey': journey,
        'total_points': len(journey)
    })

@app.route('/api/gps/eta')
def api_gps_eta():
    """API endpoint to calculate ETA"""
    current_lat = float(request.args.get('lat', 19.0760))
    current_lng = float(request.args.get('lng', 72.8777))
    dest_lat = float(request.args.get('dest_lat', 19.1136))
    dest_lng = float(request.args.get('dest_lng', 72.8697))
    
    eta = GPSTracker.estimate_arrival_time(current_lat, current_lng, dest_lat, dest_lng)
    return jsonify(eta)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ==================== RUN APP ====================

if __name__ == '__main__':
    app.run(debug=True)
