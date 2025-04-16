from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
from datetime import datetime
import uuid
import requests
from werkzeug.utils import secure_filename

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'car_images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# USD to INR conversion rate (you may want to use a real-time API in production)
USD_TO_INR_RATE = 83.0  # Fixed conversion rate

def get_car_image(make, model):
    # Generate a standardized filename based on make and model
    filename = f"{make.lower()}_{model.lower().replace(' ', '_')}_2022.jpg"
    # Check if image exists, if not return a default image
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(image_path):
        return f'/static/car_images/{filename}'
    return '/static/car_images/default_car.jpg'

app = Flask(__name__)
app.secret_key = 'car_rental_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Data storage (in-memory instead of database)
class DataStore:
    def __init__(self):
        self.cars = []
        self.users = []
        self.bookings = []
        self.load_data()

    def load_data(self):
        # Load initial data or from files if they exist
        if os.path.exists('cars.json'):
            with open('cars.json', 'r') as f:
                self.cars = json.load(f)
        else:
            # Sample car data
            self.cars = [
                {
                    'id': '1',
                    'make': 'Toyota',
                    'model': 'Corolla',
                    'year': 2020,
                    'price_per_day': 50,
                    'available': True,
                    'image': get_car_image('Toyota', 'Corolla')
                },
                {
                    'id': '2',
                    'make': 'Honda',
                    'model': 'Civic',
                    'year': 2021,
                    'price_per_day': 55,
                    'available': True,
                    'image': get_car_image('Honda', 'Civic')
                },
                {
                    'id': '3',
                    'make': 'Ford',
                    'model': 'Mustang',
                    'year': 2019,
                    'price_per_day': 80,
                    'available': True,
                    'image': get_car_image('Ford', 'Mustang')
                },
                {
                    'id': '4',
                    'make': 'BMW',
                    'model': '3 Series',
                    'year': 2022,
                    'price_per_day': 100,
                    'available': True,
                    'image': get_car_image('BMW', '3 Series')
                },
                {
                    'id': '5',
                    'make': 'Tesla',
                    'model': 'Model 3',
                    'year': 2022,
                    'price_per_day': 120,
                    'available': True,
                    'image': get_car_image('Tesla', 'Model 3')
                }
            ]
            self.save_cars()

        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        else:
            # Sample user data
            self.users = [
                {
                    'id': '1',
                    'username': 'admin',
                    'password': 'admin123',
                    'is_admin': True
                },
                {
                    'id': '2',
                    'username': 'user',
                    'password': 'user123',
                    'is_admin': False
                }
            ]
            self.save_users()

        if os.path.exists('bookings.json'):
            with open('bookings.json', 'r') as f:
                self.bookings = json.load(f)
        else:
            self.bookings = []
            self.save_bookings()

    def save_cars(self):
        with open('cars.json', 'w') as f:
            json.dump(self.cars, f)

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    def save_bookings(self):
        with open('bookings.json', 'w') as f:
            json.dump(self.bookings, f)

# Initialize data store
data_store = DataStore()

# Routes
@app.route('/')
def home():
    search_query = request.args.get('search', '').lower()
    sort_by = request.args.get('sort', 'price_asc')
    make_filter = request.args.get('make', '')

    filtered_cars = data_store.cars

    # Apply search filter
    if search_query:
        filtered_cars = [
            car for car in data_store.cars
            if search_query in car['make'].lower() or
               search_query in car['model'].lower() or
               search_query in str(car['year'])
        ]

    # Apply make filter
    if make_filter:
        filtered_cars = [
            car for car in filtered_cars
            if car['make'] == make_filter
        ]

    # Convert prices to INR
    for car in filtered_cars:
        car['price_inr'] = round(car['price_per_day'] * USD_TO_INR_RATE, 2)

    # Apply sorting
    if sort_by == 'price_asc':
        filtered_cars = sorted(filtered_cars, key=lambda x: x['price_per_day'])
    elif sort_by == 'price_desc':
        filtered_cars = sorted(filtered_cars, key=lambda x: x['price_per_day'], reverse=True)
    elif sort_by == 'year_desc':
        filtered_cars = sorted(filtered_cars, key=lambda x: x['year'], reverse=True)
    elif sort_by == 'year_asc':
        filtered_cars = sorted(filtered_cars, key=lambda x: x['year'])

    return render_template('index.html', cars=filtered_cars)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in data_store.users:
            if user['username'] == username and user['password'] == password:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = user['is_admin']
                flash('Login successful!')
                return redirect(url_for('home'))

        flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        for user in data_store.users:
            if user['username'] == username:
                flash('Username already exists')
                return render_template('register.html')

        # Create new user
        new_user = {
            'id': str(len(data_store.users) + 1),
            'username': username,
            'password': password,
            'is_admin': False
        }

        data_store.users.append(new_user)
        data_store.save_users()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/car/<car_id>')
def car_details(car_id):
    car = next((car for car in data_store.cars if car['id'] == car_id), None)
    if car:
        # Convert price to INR
        car['price_inr'] = round(car['price_per_day'] * USD_TO_INR_RATE, 2)

        # Find similar cars (same make or similar price range)
        similar_cars = []
        for other_car in data_store.cars:
            if other_car['id'] != car_id and other_car['available']:
                # Same make or similar price range (±20%)
                if (other_car['make'] == car['make'] or
                    (other_car['price_per_day'] >= car['price_per_day'] * 0.8 and
                     other_car['price_per_day'] <= car['price_per_day'] * 1.2)):
                    # Convert price to INR for similar cars
                    other_car['price_inr'] = round(other_car['price_per_day'] * USD_TO_INR_RATE, 2)
                    similar_cars.append(other_car)
                    # Limit to 3 similar cars
                    if len(similar_cars) >= 3:
                        break

        return render_template('car_details.html', car=car, cars=data_store.cars, similar_cars=similar_cars)
    flash('Car not found')
    return redirect(url_for('home'))

@app.route('/book/<car_id>', methods=['GET', 'POST'])
def book_car(car_id):
    if 'user_id' not in session:
        flash('Please login to book a car')
        return redirect(url_for('login'))

    car = next((car for car in data_store.cars if car['id'] == car_id), None)
    if not car:
        flash('Car not found')
        return redirect(url_for('home'))

    if not car['available']:
        flash('Car is not available for booking')
        return redirect(url_for('car_details', car_id=car_id))

    # Convert price to INR
    car['price_inr'] = round(car['price_per_day'] * USD_TO_INR_RATE, 2)

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Calculate total days and price
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        duration = end - start

        if duration.days < 0:
            flash('End date must be after start date')
            return render_template('book_car.html', car=car, today=datetime.now().strftime('%Y-%m-%d'))

        total_days = duration.days + 1  # Including both start and end days
        total_price = total_days * car['price_per_day'] * USD_TO_INR_RATE

        # Create booking
        booking = {
            'id': str(uuid.uuid4()),
            'car_id': car_id,
            'user_id': session['user_id'],
            'start_date': start_date,
            'end_date': end_date,
            'total_days': total_days,
            'total_price': total_price,
            'status': 'confirmed',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        data_store.bookings.append(booking)
        data_store.save_bookings()

        # Update car availability
        car['available'] = False
        data_store.save_cars()

        flash('Booking confirmed!')
        return redirect(url_for('my_bookings'))

    return render_template('book_car.html', car=car, today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        flash('Please login to view your bookings')
        return redirect(url_for('login'))

    user_bookings = []
    for booking in data_store.bookings:
        if booking['user_id'] == session['user_id']:
            # Get car details
            car = next((car for car in data_store.cars if car['id'] == booking['car_id']), None)
            if car:
                booking_with_car = booking.copy()
                booking_with_car['car'] = car
                user_bookings.append(booking_with_car)

    return render_template('my_bookings.html', bookings=user_bookings)

@app.route('/cancel-booking/<booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        flash('Please login to cancel a booking')
        return redirect(url_for('login'))

    booking = next((booking for booking in data_store.bookings if booking['id'] == booking_id), None)
    if not booking or booking['user_id'] != session['user_id']:
        flash('Booking not found or not authorized')
        return redirect(url_for('my_bookings'))

    # Update booking status
    booking['status'] = 'cancelled'

    # Make car available again
    car = next((car for car in data_store.cars if car['id'] == booking['car_id']), None)
    if car:
        car['available'] = True
        data_store.save_cars()

    data_store.save_bookings()

    flash('Booking cancelled successfully')
    return redirect(url_for('my_bookings'))

# Admin routes
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Admin access required')
        return redirect(url_for('home'))

    return render_template('admin/dashboard.html',
                           cars=data_store.cars,
                           users=data_store.users,
                           bookings=data_store.bookings)

@app.route('/admin/cars')
def admin_cars():
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Admin access required')
        return redirect(url_for('home'))

    return render_template('admin/cars.html', cars=data_store.cars)

@app.route('/admin/add-car', methods=['GET', 'POST'])
def admin_add_car():
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Admin access required')
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Handle image upload
        car_image = request.files['car_image']
        image_url = f"https://via.placeholder.com/150?text={request.form['make']}+{request.form['model']}"

        if car_image and allowed_file(car_image.filename):
            filename = secure_filename(f"{uuid.uuid4()}_{car_image.filename}")
            car_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('static', filename=f'car_images/{filename}')

        new_car = {
            'id': str(len(data_store.cars) + 1),
            'make': request.form['make'],
            'model': request.form['model'],
            'year': int(request.form['year']),
            'price_per_day': float(request.form['price_per_day']),
            'available': True,
            'image': image_url
        }

        data_store.cars.append(new_car)
        data_store.save_cars()

        flash('Car added successfully')
        return redirect(url_for('admin_cars'))

    return render_template('admin/add_car.html')

@app.route('/admin/edit-car/<car_id>', methods=['GET', 'POST'])
def admin_edit_car(car_id):
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Admin access required')
        return redirect(url_for('home'))

    car = next((car for car in data_store.cars if car['id'] == car_id), None)
    if not car:
        flash('Car not found')
        return redirect(url_for('admin_cars'))

    if request.method == 'POST':
        car['make'] = request.form['make']
        car['model'] = request.form['model']
        car['year'] = int(request.form['year'])
        car['price_per_day'] = float(request.form['price_per_day'])
        car['available'] = 'available' in request.form
        car['image'] = request.form['image'] or car['image']

        data_store.save_cars()

        flash('Car updated successfully')
        return redirect(url_for('admin_cars'))

    return render_template('admin/edit_car.html', car=car)

@app.route('/admin/delete-car/<car_id>')
def admin_delete_car(car_id):
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Admin access required')
        return redirect(url_for('home'))

    car_index = next((i for i, car in enumerate(data_store.cars) if car['id'] == car_id), None)
    if car_index is not None:
        data_store.cars.pop(car_index)
        data_store.save_cars()
        flash('Car deleted successfully')
    else:
        flash('Car not found')

    return redirect(url_for('admin_cars'))

@app.route('/admin/bookings')
def admin_bookings():
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Admin access required')
        return redirect(url_for('home'))

    bookings_with_details = []
    for booking in data_store.bookings:
        # Get car details
        car = next((car for car in data_store.cars if car['id'] == booking['car_id']), None)
        # Get user details
        user = next((user for user in data_store.users if user['id'] == booking['user_id']), None)

        if car and user:
            booking_with_details = booking.copy()
            booking_with_details['car'] = car
            booking_with_details['user'] = user
            bookings_with_details.append(booking_with_details)

    return render_template('admin/bookings.html', bookings=bookings_with_details)

@app.route('/admin/update-booking/<booking_id>', methods=['POST'])
def admin_update_booking(booking_id):
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Admin access required')
        return redirect(url_for('home'))

    booking = next((booking for booking in data_store.bookings if booking['id'] == booking_id), None)
    if not booking:
        flash('Booking not found')
        return redirect(url_for('admin_bookings'))

    status = request.form['status']
    booking['status'] = status

    # If cancelled, make car available again
    if status == 'cancelled':
        car = next((car for car in data_store.cars if car['id'] == booking['car_id']), None)
        if car:
            car['available'] = True
            data_store.save_cars()

    data_store.save_bookings()

    flash('Booking status updated successfully')
    return redirect(url_for('admin_bookings'))

if __name__ == '__main__':
    app.run(debug=True)