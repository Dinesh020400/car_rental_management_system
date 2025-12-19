# Car Rental Management System - Setup Guide

## New Features Added

### 1. **MongoDB Database Integration**
- Migrated from JSON files to MongoDB
- Collections: users, cars, bookings, payments, otps
- Automatic data migration from existing JSON files

### 2. **Password Security**
- Passwords are now hashed using bcrypt
- Secure password verification
- Password change functionality

### 3. **Email OTP Verification**
- Email verification using OTP (One-Time Password)
- OTP expires in 10 minutes
- Resend OTP functionality
- Verification required on registration

### 4. **User Profile Management**
- View and edit profile
- Update email and phone number
- Upload profile picture
- Change password securely

### 5. **Payment Integration (Simplified)**
- Support for UPI, Card, and Wallet payments
- Payment processing simulation
- Transaction ID generation
- Payment status tracking
- Refund processing for cancellations

### 6. **Invoice Generation**
- Automatic PDF invoice generation using ReportLab
- Professional invoice design with GST calculation
- Download invoice after booking
- Email invoice to customer

## Installation Steps

### 1. Install MongoDB
Download and install MongoDB Community Server from:
https://www.mongodb.com/try/download/community

**Windows Installation:**
```powershell
# Download MongoDB installer
# Install MongoDB Community Server
# MongoDB will run on mongodb://localhost:27017/
```

### 2. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Edit the `.env` file with your settings:

```
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=car_rental_db

# Email Configuration (for OTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com

# Secret Key
SECRET_KEY=your_secret_key_here
```

**Getting Gmail App Password:**
1. Go to Google Account settings
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate a new app password for "Mail"
5. Use that password in MAIL_PASSWORD

### 4. Run the Application

**Option 1: Use the new integrated app (Recommended)**
```powershell
python app_new.py
```

**Option 2: Backup and replace old app.py**
```powershell
# Backup old app
Copy-Item app.py app_old.py

# Replace with new app
Copy-Item app_new.py app.py -Force

# Run app
python app.py
```

### 5. Migrate Existing Data
Once the app is running, visit:
```
http://localhost:5000/admin/migrate-data
```
This will migrate all existing users, cars, and bookings from JSON files to MongoDB.

**Note:** You need to login as admin first:
- Username: admin
- Password: admin123

## Project Structure

```
car_rental_management_system/
│
├── app_new.py                 # New integrated Flask app
├── config.py                  # Configuration management
├── database.py               # MongoDB connection & migration
├── auth_service.py           # Authentication & password hashing
├── email_service.py          # Email & OTP functionality
├── profile_service.py        # User profile management
├── payment_service.py        # Payment processing
├── invoice_service.py        # PDF invoice generation
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
│
├── templates/
│   ├── verify_email.html     # Email verification page
│   ├── profile.html          # User profile page
│   ├── edit_profile.html     # Edit profile page
│   ├── payment.html          # Payment page
│   ├── booking_success.html  # Success page
│   └── ... (existing templates)
│
└── static/
    ├── invoices/             # Generated invoices
    └── profile_pictures/     # User profile pictures
```

## Features Overview

### Authentication Flow
1. **Register** → Email/Phone/Password
2. **Email Verification** → OTP sent to email
3. **Verify OTP** → Account activated
4. **Login** → Secure password verification

### Booking Flow
1. **Browse Cars** → Search and filter
2. **Select Car** → View details
3. **Book Car** → Select dates
4. **Payment** → Choose payment method (UPI/Card/Wallet)
5. **Confirmation** → Receive email + invoice
6. **Download Invoice** → PDF invoice

### Profile Management
1. **View Profile** → See all details
2. **Edit Profile** → Update email/phone
3. **Upload Picture** → Profile photo
4. **Change Password** → Secure password update

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /verify-otp` - Verify email OTP
- `POST /resend-otp` - Resend OTP
- `POST /login` - User login
- `GET /logout` - User logout

### Profile
- `GET /profile` - View profile
- `GET /profile/edit` - Edit profile page
- `POST /profile/edit` - Update profile
- `POST /profile/change-password` - Change password

### Booking & Payment
- `POST /book/<car_id>` - Create booking
- `GET /payment/<booking_id>` - Payment page
- `POST /process-payment/<booking_id>` - Process payment
- `GET /booking-success/<booking_id>` - Success page
- `GET /download-invoice/<booking_id>` - Download PDF

### Admin
- `GET /admin/migrate-data` - Migrate JSON to MongoDB

## Payment Methods

The system supports three payment methods:

1. **UPI** - Unified Payments Interface
   - Simulates UPI payment
   - QR code generation (mock)

2. **Card** - Credit/Debit Card
   - Card details form (simplified)
   - Secure processing simulation

3. **Wallet** - Digital Wallets
   - PayTM, PhonePe, GooglePay, AmazonPay
   - Wallet selection interface

**Note:** This is a simplified payment gateway implementation. In production, integrate with real payment providers like:
- Razorpay
- Paytm Payment Gateway
- Stripe
- PayU

## Invoice Features

- Professional PDF layout
- Company branding
- Customer details
- Booking information
- Price breakdown with GST
- Transaction details
- Downloadable PDF
- Email delivery

## Security Features

1. **Password Hashing** - bcrypt with salt
2. **Session Management** - Flask sessions
3. **Email Verification** - OTP-based
4. **Secure Payment** - Transaction tracking
5. **MongoDB Security** - Connection URI in .env

## Testing

### Test Accounts
After migration, you can use:
- Admin: username=`admin`, password=`admin123`
- User: username=`user`, password=`user123`

**Note:** Existing passwords in JSON are plain text. After migration:
1. Users should change passwords (will be hashed)
2. Or manually update passwords in MongoDB

### Test Email OTP
Configure a real email in `.env` to test OTP functionality.

## Troubleshooting

### MongoDB Connection Error
```
pymongo.errors.ServerSelectionTimeoutError
```
**Solution:** Ensure MongoDB is running
```powershell
# Check MongoDB service
Get-Service MongoDB

# Start MongoDB
Start-Service MongoDB
```

### Email Sending Error
```
SMTPAuthenticationError
```
**Solution:** 
1. Enable 2-Step Verification in Gmail
2. Generate App Password
3. Update MAIL_PASSWORD in .env

### Import Errors
```
ModuleNotFoundError
```
**Solution:** Install all dependencies
```powershell
pip install -r requirements.txt
```

## Production Considerations

1. **Database:**
   - Use MongoDB Atlas (cloud)
   - Set up authentication
   - Configure replica sets

2. **Email:**
   - Use SendGrid, AWS SES, or Mailgun
   - Configure proper SMTP settings
   - Handle email queues

3. **Payments:**
   - Integrate real payment gateway
   - Implement webhooks
   - Handle payment failures
   - PCI compliance

4. **Security:**
   - Use HTTPS
   - Implement rate limiting
   - Add CSRF protection
   - Secure file uploads
   - Environment variable management

5. **Performance:**
   - Add caching (Redis)
   - Optimize database queries
   - Implement CDN for static files
   - Load balancing

## Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Social login (Google, Facebook)
- [ ] Real-time booking availability
- [ ] Push notifications
- [ ] Mobile app
- [ ] Advanced analytics dashboard
- [ ] Loyalty points system
- [ ] Multi-language support
- [ ] Car rating and reviews
- [ ] Insurance options
- [ ] GPS tracking integration

## Support

For issues or questions:
1. Check MongoDB connection
2. Verify .env configuration
3. Review console logs
4. Check browser console for JavaScript errors

## License

This project is licensed under the MIT License.
