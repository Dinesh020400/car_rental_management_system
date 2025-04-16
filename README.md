# Car Rental Management System

A modern, feature-rich car rental web application built with Python and Flask. This application allows users to browse available cars, create accounts, book cars, and manage their bookings. It also includes an admin interface for managing cars, users, and bookings.

## Features

### User Features
- **User Registration and Authentication**: Create an account and login securely
- **Car Browsing**: View all available cars with filtering and sorting options
- **Car Details**: View detailed information about each car
- **Booking System**: Book cars for specific dates
- **Booking Management**: View and cancel bookings
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Admin Features
- **Dashboard**: Overview of cars, users, and bookings
- **Car Management**: Add, edit, and delete cars
- **Booking Management**: View and update booking statuses
- **User Management**: View registered users

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: JSON files (for simplicity, can be upgraded to a proper database)
- **Additional Libraries**:
  - Flatpickr (for date picking)
  - Font Awesome (for icons)

## Installation and Setup

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Dinesh020400/car_rental_management_system.git
   cd car_rental_management_system
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Default Users

The system comes with two default users:

- **Admin User**:
  - Username: `admin`
  - Password: `admin123`

- **Regular User**:
  - Username: `user`
  - Password: `user123`

## Usage Guide

### User Guide

#### Registration and Login
1. Click on the "Register" button in the navigation bar
2. Fill in your username and password
3. Click "Register" to create your account
4. Login using your credentials

#### Browsing Cars
1. The homepage displays all available cars
2. Use the search bar to find specific cars by make, model, or year
3. Use the filter options to sort by price or year
4. Click on "View Details" to see more information about a car

#### Booking a Car
1. Navigate to the car details page
2. Click on "Book Now"
3. Select your pickup and return dates
4. Review the booking summary
5. Click "Confirm Booking" to complete your reservation

#### Managing Bookings
1. Click on "My Bookings" in the navigation bar
2. View all your bookings with their status
3. Cancel a booking by clicking the "Cancel" button if needed
4. View car details by clicking "View Car"

#### Using Dark Mode
- Click on the moon/sun icon in the navigation bar to toggle between light and dark mode

### Admin Guide

#### Accessing Admin Dashboard
1. Login with admin credentials:
   - Username: `admin`
   - Password: `admin123`
2. Click on "Admin" in the navigation bar

#### Managing Cars
1. From the admin dashboard, click "Manage Cars"
2. View all cars in the system
3. Add a new car by clicking "Add New Car"
4. Edit or delete existing cars using the action buttons

#### Managing Bookings
1. From the admin dashboard, click "Manage Bookings"
2. View all bookings in the system
3. Update booking status using the dropdown and "Update" button

## Project Structure

```
car_rental_management_system/
├── app.py                  # Main application file
├── static/                 # Static files
│   └── car_images/         # Car images
├── templates/              # HTML templates
│   ├── admin/              # Admin templates
│   │   ├── add_car.html
│   │   ├── bookings.html
│   │   ├── cars.html
│   │   ├── dashboard.html
│   │   └── edit_car.html
│   ├── base.html           # Base template
│   ├── book_car.html       # Booking form
│   ├── car_details.html    # Car details page
│   ├── index.html          # Homepage
│   ├── login.html          # Login page
│   ├── my_bookings.html    # User bookings page
│   └── register.html       # Registration page
├── cars.json               # Car data storage
├── users.json              # User data storage
├── bookings.json           # Booking data storage
└── requirements.txt        # Project dependencies
```

## Data Storage

All data is stored in JSON files in the project directory:
- **cars.json**: Stores information about all cars
- **users.json**: Stores user account information
- **bookings.json**: Stores all booking information

These files are created automatically when the application runs for the first time.

In a production environment, you might want to replace this with a proper database system like SQLite, PostgreSQL, or MongoDB.

## Customization

### Adding New Cars

As an admin, you can add new cars through the admin interface. Alternatively, you can edit the `cars.json` file directly or modify the initial data in the `DataStore` class in `app.py`.

### Changing the Theme

The color scheme can be modified by editing the CSS variables in the `base.html` file:

```css
:root {
    --primary-color: #3B82F6;
    --primary-dark: #2563EB;
    --secondary-color: #10B981;
    --secondary-dark: #059669;
    /* other variables */
}
```

## UI Features

### Modern Design
- Clean and intuitive interface
- Card-based layout for better visual organization
- Consistent styling throughout the application

### Responsive Layout
- Mobile-friendly design that adapts to different screen sizes
- Optimized navigation for small screens

### Interactive Elements
- Real-time booking summary updates
- Enhanced date pickers
- Dropdown menus for better space utilization

### Visual Feedback
- Status badges for bookings
- Clear call-to-action buttons
- Informative alerts and notifications

## Future Enhancements

Potential improvements for future versions:

1. **Database Integration**: Replace JSON files with a proper database
2. **User Profiles**: Allow users to update their profile information
3. **Payment Integration**: Add payment processing for bookings
4. **Email Notifications**: Send booking confirmations and reminders
5. **Reviews and Ratings**: Allow users to rate and review cars
6. **Advanced Filtering**: More filtering options for car search
7. **Multiple Images**: Support multiple images for each car
8. **Availability Calendar**: Visual calendar showing car availability

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please contact:
- GitHub: [Dinesh020400](https://github.com/Dinesh020400)