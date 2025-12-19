# 🚗 Car Rental Management System

A modern, full-featured car rental management system built with Flask, MongoDB, and advanced features including GPS tracking, analytics, professional invoicing, and more.

## ✨ Key Highlights

- 🎨 **Modern UI**: Gradient design with smooth animations
- 📊 **Analytics Dashboard**: Comprehensive statistics with Chart.js
- 🗺️ **GPS Tracking**: Real-time vehicle tracking (admin only)
- 📄 **Professional Invoices**: Auto-generated PDF with GST details
- 📧 **Email Notifications**: Automated emails with attachments
- 💳 **Payment Integration**: Multiple payment methods (UPI/Card/Wallet)
- ⭐ **Review System**: User ratings and feedback
- 🔐 **Security**: Bcrypt password hashing and email verification
- **Profile Management**: Edit email, phone, upload photo
- **Booking Management**: View and cancel bookings with refunds
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works on desktop, tablet, and mobile

### Admin Features
- **Dashboard**: Overview of cars, users, and bookings
- **Car Management**: Add, edit, and delete cars
- **Booking Management**: View and update booking statuses
- **User Management**: View registered users
- **Data Migration**: Migrate JSON data to MongoDB

## 🛠️ Technology Stack

- **Backend**: Flask 2.3.3, Python 3.x
- **Database**: MongoDB with PyMongo
- **Email**: Flask-Mail with threading
- **PDF Generation**: ReportLab
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Maps**: Leaflet.js for GPS tracking
- **Charts**: Chart.js for analytics
- **Styling**: Custom gradient theme (#667eea → #764ba2)
- **Security**: Bcrypt password hashing

## 📁 Project Structure

```
car_rental_management_system/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # MongoDB connection
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── services/                   # Service layer modules
│   ├── analytics_service.py
│   ├── auth_service.py
│   ├── email_service.py
│   ├── enhanced_notification.py
│   ├── gps_tracker.py
│   ├── invoice_service_pro.py
│   ├── location_service.py
│   ├── payment_service.py
│   ├── profile_service.py
│   └── review_service.py
├── static/                     # Static assets
│   ├── car_images/
│   └── invoices/
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── admin/
└── docs/                       # Documentation
    ├── SETUP_GUIDE.md
    ├── QUICKSTART.md
    └── ...
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MongoDB (local or Atlas)
- SMTP server for emails

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   
   Create/edit `.env` file:
   ```env
   SECRET_KEY=your-secret-key
   MONGODB_URI=mongodb://localhost:27017/car_rental
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

3. **Run application**
   ```bash
   python app.py
   ```

4. **Access**
   - User: http://127.0.0.1:5000
   - Admin: http://127.0.0.1:5000/admin
   - Default admin: username `admin`, password `admin123`

## 📚 Features

### For Users
- Browse and search cars with filters
- Make bookings with date/time selection
- Multiple payment methods (UPI/Card/Wallet)
- Download professional PDF invoices
- Track booking history
- Add reviews and ratings
- Update profile with photo upload
- Receive email notifications

### For Admins
- Dashboard with comprehensive statistics
- Manage cars (add, edit, delete)
- View and manage all bookings
- Track vehicles with GPS (real-time)
- Analytics dashboard with charts
- User management
- Revenue tracking

## 📖 Documentation

Detailed guides available in the `docs/` folder:
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Quick Start](docs/QUICKSTART.md)
- [Implementation Details](docs/IMPLEMENTATION.md)
- [New Features](docs/NEW_FEATURES.md)
- [Fixes & Alerts](docs/FIXES_AND_ALERTS_GUIDE.md)
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

## 🎨 UI Theme

The application features a modern gradient design system:
- **Primary Gradient**: #667eea → #764ba2 (Purple)
- **Typography**: Poppins, Space Grotesk
- **Components**: Bootstrap 5 with custom CSS
- **Animations**: Smooth transitions, hover effects, lift animations
- **Responsive**: Mobile-first design approach

## 🔐 Default Credentials

- **Admin**: username `admin`, password `admin123`
- **User**: Create your own account via registration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask documentation
- MongoDB documentation
- Bootstrap framework
- Leaflet.js mapping library
- Chart.js visualization library

---

**Made with ❤️ for efficient car rental management**