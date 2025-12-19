# 🚗 Car Rental Management System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green?logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4.6%2B-darkgreen?logo=mongodb&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![GitHub repo size](https://img.shields.io/github/repo-size/Dinesh020400/car_rental_management_system)
![GitHub last commit](https://img.shields.io/github/last-commit/Dinesh020400/car_rental_management_system)

A modern, full-featured car rental management system built with Flask, MongoDB, and advanced features including GPS tracking, analytics, professional invoicing, and more.

**Language Composition:** HTML (65.9%) • Python (32.2%) • CSS (1.6%) • Batchfile (0.3%)

---

## 📑 Table of Contents

- [✨ Key Highlights](#-key-highlights)
- [🎯 Features](#-features)
  - [User Features](#user-features)
  - [Admin Features](#admin-features)
- [🛠️ Technology Stack](#-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Installation & Setup](#-installation--setup)
- [📖 Usage Guide](#-usage-guide)
- [📸 Screenshots](#-screenshots)
- [📚 Documentation](#-documentation)
- [🎨 UI Theme](#-ui-theme)
- [🔮 Future Enhancements](#-future-enhancements)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [👤 Contact](#-contact)

---

## ✨ Key Highlights

- 🎨 **Modern UI**: Gradient design with smooth animations and intuitive interface
- 📊 **Analytics Dashboard**: Comprehensive statistics with Chart.js visualizations
- 🗺️ **GPS Tracking**: Real-time vehicle tracking with Leaflet.js (admin only)
- 📄 **Professional Invoices**: Auto-generated PDF invoices with GST details
- 📧 **Email Notifications**: Automated emails with attachments and threading
- 💳 **Payment Integration**: Multiple payment methods (UPI/Card/Wallet)
- ⭐ **Review System**: User ratings and feedback with moderation
- 🔐 **Security**: Bcrypt password hashing and email verification
- 👤 **Profile Management**: Edit email, phone, and upload profile photo
- 📅 **Booking Management**: View and cancel bookings with automated refunds
- 🌓 **Dark Mode**: Toggle between light and dark themes
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

---

## 🎯 Features

### User Features

- 🔑 **User Registration & Authentication**: Secure account creation and login with bcrypt encryption
- 🚗 **Car Browsing**: View all available cars with advanced filtering and sorting options
- 🔍 **Car Details**: Comprehensive car information with images and specifications
- 📆 **Booking System**: Book cars for specific dates with enhanced date picker
- 💳 **Payment Options**: Multiple payment methods including UPI, Card, and Wallet
- 📄 **Invoice Generation**: Download professional PDF invoices with GST details
- 📧 **Email Notifications**: Receive booking confirmations and updates via email
- ⭐ **Review & Rating**: Rate and review cars after rental completion
- 👤 **Profile Management**: Update personal information and upload profile photo
- 📱 **My Bookings**: Track booking history with status updates and cancellation options
- 🌓 **Dark Mode**: Toggle between light and dark themes for comfortable viewing
- 📱 **Responsive UI**: Mobile-friendly design that adapts to all screen sizes

### Admin Features

- 📊 **Dashboard**: Comprehensive overview with statistics and charts
- 🚗 **Car Management**: Add, edit, and delete cars with image upload
- 📋 **Booking Management**: View and update booking statuses
- 👥 **User Management**: View registered users and their activities
- 🗺️ **GPS Tracking**: Real-time vehicle tracking on interactive maps
- 📈 **Analytics**: Revenue tracking, booking trends, and usage statistics
- 📧 **Email Management**: Control notification settings and templates
- 🔄 **Data Migration**: Tools to migrate JSON data to MongoDB
- 📊 **Reports**: Generate detailed reports on bookings and revenue

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Language**: Python 3.8+
- **Database**: MongoDB 4.6+ with PyMongo
- **Email**: Flask-Mail with threading support
- **PDF Generation**: ReportLab 4.0.7
- **Authentication**: Bcrypt 4.1.2
- **Environment**: python-dotenv 1.0.0

### Frontend
- **UI Framework**: Bootstrap 5
- **Languages**: HTML5, CSS3, JavaScript
- **Date Picker**: Flatpickr
- **Icons**: Font Awesome
- **Maps**: Leaflet.js for GPS tracking
- **Charts**: Chart.js for analytics
- **Typography**: Poppins, Space Grotesk fonts

### Additional Tools
- **Version Control**: Git
- **Package Manager**: pip
- **Server**: Flask development server (or production WSGI server)

---

## 📁 Project Structure

```
car_rental_management_system/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # MongoDB connection and setup
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # This file
├── run.bat                     # Windows startup script
├── setup.bat                   # Windows setup script
│
├── services/                   # Service layer modules
│   ├── __init__.py
│   ├── analytics_service.py    # Analytics and statistics
│   ├── auth_service.py         # Authentication logic
│   ├── email_service.py        # Email sending functionality
│   ├── enhanced_notification.py # Advanced notifications
│   ├── gps_tracker.py          # GPS tracking service
│   ├── invoice_service_pro.py  # Professional invoice generation
│   ├── location_service.py     # Location-based services
│   ├── payment_service.py      # Payment processing
│   ├── profile_service.py      # User profile management
│   └── review_service.py       # Review and rating system
│
├── static/                     # Static assets
│   ├── car_images/             # Car images storage
│   ├── invoices/               # Generated PDF invoices
│   └── css/                    # Custom stylesheets
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template with navbar
│   ├── index.html              # Homepage
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── car_details.html        # Car details page
│   ├── book_car.html           # Booking form
│   ├── booking_success.html    # Booking confirmation
│   ├── my_bookings.html        # User bookings page
│   ├── profile.html            # User profile
│   ├── edit_profile.html       # Profile editing
│   ├── payment.html            # Payment page
│   ├── add_review.html         # Add review page
│   ├── my_reviews.html         # User reviews
│   ├── track_vehicle.html      # GPS tracking page
│   ├── verify_email.html       # Email verification
│   ├── 404.html                # 404 error page
│   ├── 500.html                # 500 error page
│   └── admin/                  # Admin templates
│       ├── dashboard.html
│       ├── cars.html
│       ├── add_car.html
│       ├── edit_car.html
│       ├── bookings.html
│       ├── users.html
│       └── analytics.html
│
├── docs/                       # Documentation
│   ├── SETUP_GUIDE.md          # Detailed setup instructions
│   ├── QUICKSTART.md           # Quick start guide
│   ├── IMPLEMENTATION.md       # Implementation details
│   ├── NEW_FEATURES.md         # New features documentation
│   ├── FIXES_AND_ALERTS_GUIDE.md # Troubleshooting guide
│   └── GITHUB_GUIDE.md         # GitHub workflow guide
│
└── [JSON files]                # Data storage (legacy/backup)
    ├── cars.json
    ├── users.json
    └── bookings.json
```

---

## 🚀 Installation & Setup

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **MongoDB** (local installation or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account)
- **Git** (for cloning the repository)
- **SMTP Server** access for email functionality (e.g., Gmail)

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/Dinesh020400/car_rental_management_system.git
cd car_rental_management_system
```

#### 2. Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following configuration:

```env
# Application Settings
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=development
DEBUG=True

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/car_rental
# Or for MongoDB Atlas:
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/car_rental

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Application URLs
BASE_URL=http://127.0.0.1:5000
```

**Note for Gmail users**: You need to generate an [App Password](https://support.google.com/accounts/answer/185833) instead of using your regular password.

#### 5. Set Up MongoDB

**Option A: Local MongoDB**
- Install MongoDB on your system
- Start MongoDB service: `mongod`
- Database will be created automatically on first run

**Option B: MongoDB Atlas (Cloud)**
- Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Create a cluster and get your connection string
- Update `MONGODB_URI` in `.env` file

#### 6. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

#### 7. Access the Application

- **User Interface**: `http://127.0.0.1:5000`
- **Admin Dashboard**: `http://127.0.0.1:5000/admin`

### 🔐 Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Regular User Account:**
- Username: `user`
- Password: `user123`

**⚠️ Important**: Change default passwords after first login for security!

---

## 📖 Usage Guide

### For Users

#### 1. Registration and Login
1. Navigate to the homepage
2. Click "Register" in the navigation bar
3. Fill in your details (username, email, password)
4. Verify your email address (check spam folder)
5. Login with your credentials

#### 2. Browsing and Searching Cars
1. Browse all available cars on the homepage
2. Use the search bar to find specific cars by make, model, or year
3. Apply filters to sort by price, year, or availability
4. Click "View Details" for comprehensive car information

#### 3. Booking a Car
1. From car details page, click "Book Now"
2. Select pickup and return dates using the date picker
3. Review the booking summary and price calculation
4. Choose your preferred payment method
5. Complete payment (UPI/Card/Wallet)
6. Download your PDF invoice

#### 4. Managing Your Bookings
1. Click "My Bookings" in the navigation bar
2. View all your bookings with status indicators
3. Download invoices for completed bookings
4. Cancel upcoming bookings (refund policies apply)
5. Add reviews after rental completion

#### 5. Profile Management
1. Click on your profile icon
2. Update personal information (email, phone)
3. Upload profile photo
4. View booking history and statistics

#### 6. Adding Reviews
1. Complete a rental booking
2. Navigate to "My Bookings"
3. Click "Add Review" on completed bookings
4. Rate the car (1-5 stars) and write your feedback

### For Admins

#### 1. Accessing Admin Dashboard
1. Login with admin credentials
2. Click "Admin" in the navigation bar
3. View comprehensive dashboard with statistics

#### 2. Managing Cars
1. From admin dashboard, select "Manage Cars"
2. **Add New Car**: Click "Add New Car" button
   - Fill in car details (make, model, year, price, etc.)
   - Upload car image
   - Set availability status
3. **Edit Car**: Click edit icon on any car
4. **Delete Car**: Click delete icon (with confirmation)

#### 3. Managing Bookings
1. Select "Manage Bookings" from admin menu
2. View all bookings with user details
3. Update booking status (Pending/Confirmed/Completed/Cancelled)
4. Filter bookings by status or date
5. View booking analytics and trends

#### 4. GPS Vehicle Tracking
1. Navigate to "Track Vehicles"
2. View real-time location of all rented vehicles
3. Click on vehicle markers for details
4. Monitor vehicle routes and history

#### 5. Analytics Dashboard
1. Access "Analytics" from admin menu
2. View revenue trends and charts
3. Analyze booking patterns
4. Generate reports for specific periods
5. Export data for further analysis

#### 6. User Management
1. Select "Users" from admin menu
2. View all registered users
3. Monitor user activity and booking history
4. Manage user permissions (if applicable)

---

## 📸 Screenshots

*Screenshots will be added here to showcase the application's interface:*

- Homepage with car listings
- Car details page
- Booking process
- Admin dashboard
- GPS tracking interface
- Analytics charts
- Mobile responsive views

*(To be updated with actual screenshots)*

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[📘 Setup Guide](docs/SETUP_GUIDE.md)**: Detailed installation and configuration instructions
- **[🚀 Quick Start Guide](docs/QUICKSTART.md)**: Get started quickly with minimal setup
- **[💻 Implementation Details](docs/IMPLEMENTATION.md)**: Technical implementation documentation
- **[✨ New Features](docs/NEW_FEATURES.md)**: Latest features and updates
- **[🔧 Fixes & Alerts Guide](docs/FIXES_AND_ALERTS_GUIDE.md)**: Troubleshooting and solutions
- **[📖 GitHub Guide](docs/GITHUB_GUIDE.md)**: Git workflow and contribution guidelines

---

## 🎨 UI Theme

The application features a modern, visually appealing design system:

### Color Palette
- **Primary Gradient**: `#667eea → #764ba2` (Purple gradient)
- **Background**: Dynamic light/dark mode support
- **Accent Colors**: Complementary blues and purples

### Typography
- **Primary Font**: Poppins (headings and emphasis)
- **Secondary Font**: Space Grotesk (body text)
- **Fallback**: System fonts for optimal performance

### Design Elements
- **Components**: Bootstrap 5 with custom CSS overrides
- **Animations**: Smooth transitions and hover effects
- **Cards**: Elevated cards with lift animations
- **Buttons**: Gradient buttons with hover states
- **Forms**: Modern input styling with validation feedback
- **Responsive**: Mobile-first design approach

### Customization

To customize the theme, edit the CSS variables in `templates/base.html`:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #3B82F6;
    --success-color: #10B981;
    --warning-color: #F59E0B;
    --danger-color: #EF4444;
    --text-primary: #1F2937;
    --text-secondary: #6B7280;
    /* Add more custom variables */
}
```

---

## 🔮 Future Enhancements

Planned features and improvements for future releases:

### Phase 1: Enhanced User Experience
- [ ] **Multi-language Support**: Internationalization (i18n) for global users
- [ ] **Progressive Web App**: Offline functionality and app-like experience
- [ ] **Push Notifications**: Real-time updates via browser notifications
- [ ] **Advanced Search**: AI-powered search with recommendations
- [ ] **Wishlist Feature**: Save favorite cars for later

### Phase 2: Business Features
- [ ] **Loyalty Program**: Reward points and membership tiers
- [ ] **Corporate Accounts**: Bulk booking for businesses
- [ ] **Insurance Integration**: Optional insurance during booking
- [ ] **Dynamic Pricing**: AI-based pricing based on demand
- [ ] **Referral System**: Earn rewards for referring friends

### Phase 3: Technical Improvements
- [ ] **Microservices Architecture**: Scale individual components
- [ ] **Redis Caching**: Improve performance with caching layer
- [ ] **Real-time Chat**: Support chat for customer service
- [ ] **API Documentation**: OpenAPI/Swagger documentation
- [ ] **Mobile Apps**: Native iOS and Android applications
- [ ] **Blockchain Integration**: Transparent transaction records
- [ ] **Machine Learning**: Predictive analytics for maintenance

### Phase 4: Administrative Tools
- [ ] **Automated Reports**: Scheduled report generation and email
- [ ] **Maintenance Tracking**: Vehicle maintenance schedules
- [ ] **Fleet Management**: Advanced fleet optimization tools
- [ ] **Driver Assignment**: Assign drivers to bookings
- [ ] **Damage Assessment**: Photo-based damage reporting
- [ ] **Fuel Management**: Track fuel consumption and costs

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/car_rental_management_system.git
   cd car_rental_management_system
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style and conventions
   - Add comments where necessary
   - Update documentation if needed

5. **Test Your Changes**
   - Ensure all existing functionality works
   - Test new features thoroughly
   - Check for any breaking changes

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

7. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Provide a clear description of your changes
   - Link any related issues

### Contribution Guidelines

- **Code Style**: Follow PEP 8 for Python code
- **Commits**: Use clear, descriptive commit messages
- **Documentation**: Update README and docs for new features
- **Testing**: Ensure your code doesn't break existing functionality
- **Issues**: Check existing issues before creating new ones
- **Respect**: Be respectful and constructive in discussions

### Areas for Contribution

- 🐛 **Bug Fixes**: Fix existing bugs and issues
- ✨ **New Features**: Add new functionality
- 📝 **Documentation**: Improve or translate documentation
- 🎨 **UI/UX**: Enhance user interface and experience
- 🧪 **Testing**: Add unit tests and integration tests
- 🔒 **Security**: Identify and fix security vulnerabilities
- ⚡ **Performance**: Optimize code for better performance

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
Copyright (c) 2023 Dinesh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

**You are free to:**
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

**Under the conditions:**
- 📄 License and copyright notice must be included

---

## 👤 Contact

### Author

**Dinesh**

- 🐙 **GitHub**: [@Dinesh020400](https://github.com/Dinesh020400)
- 📧 **Email**: Available through GitHub profile
- 💼 **LinkedIn**: Connect on LinkedIn (link in GitHub profile)

### Support

For questions, suggestions, or issues:

1. **GitHub Issues**: [Report an Issue](https://github.com/Dinesh020400/car_rental_management_system/issues)
2. **Pull Requests**: [Submit a PR](https://github.com/Dinesh020400/car_rental_management_system/pulls)
3. **Discussions**: Use GitHub Discussions for general questions

---

## 🙏 Acknowledgments

Special thanks to:

- **Flask Community** - For the excellent web framework
- **MongoDB** - For the flexible database solution
- **Bootstrap Team** - For the responsive UI framework
- **Leaflet.js** - For the mapping library
- **Chart.js** - For beautiful visualizations
- **ReportLab** - For PDF generation capabilities
- **Open Source Community** - For inspiration and support

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

**Made with ❤️ by [Dinesh](https://github.com/Dinesh020400)**

**🚗 Happy Car Renting! 🚗**

</div>
