# Quick Start Guide

## Prerequisites
1. **MongoDB** - Install and run MongoDB Community Server
2. **Python 3.8+** - Python installed on your system

## Installation (5 minutes)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Configure Environment
Edit `.env` file with your email settings (for OTP verification):
```
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

**Get Gmail App Password:**
1. Google Account → Security → 2-Step Verification (enable it)
2. Search "App passwords" → Select Mail → Generate
3. Copy the 16-character password to `.env`

### Step 3: Start MongoDB
```powershell
# Windows - MongoDB should auto-start after installation
# Or manually start the service:
net start MongoDB
```

### Step 4: Migrate Data
```powershell
python migrate.py
```

### Step 5: Run Application
```powershell
python app_new.py
```

### Step 6: Access Application
Open browser: `http://localhost:5000`

## Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**User Account:**
- Username: `user`
- Password: `user123`

## New Features

✅ **MongoDB Database** - No more JSON files  
✅ **Password Hashing** - Secure bcrypt encryption  
✅ **Email OTP** - Verification on registration  
✅ **User Profiles** - Edit email, phone, upload photo  
✅ **Payment Gateway** - UPI, Card, Wallet support  
✅ **Invoice Generation** - PDF invoices with GST  

## File Structure

```
Important Files:
├── app_new.py           ← Main application (NEW)
├── migrate.py           ← Run this first to migrate data
├── .env                 ← Configure email here
├── config.py            ← Configuration
├── database.py          ← MongoDB connection
├── auth_service.py      ← Password hashing
├── email_service.py     ← Email & OTP
├── payment_service.py   ← Payments
├── invoice_service.py   ← PDF invoices
└── SETUP_GUIDE.md       ← Detailed documentation
```

## Testing the Features

### 1. Register New User
- Go to Register page
- Enter: username, email, phone, password
- Check email for OTP
- Verify OTP to activate account

### 2. Book a Car
- Browse available cars
- Select a car and click "Book"
- Choose dates
- Proceed to payment
- Select payment method (UPI/Card/Wallet)
- Complete booking
- Download invoice

### 3. Manage Profile
- Click on Profile
- Edit email, phone
- Upload profile picture
- Change password

### 4. Admin Functions
- Login as admin
- Access /admin dashboard
- Manage cars, bookings, users
- Migrate data: /admin/migrate-data

## Troubleshooting

**MongoDB not connecting?**
```powershell
# Check if MongoDB is running
Get-Service MongoDB

# Start MongoDB service
net start MongoDB
```

**Email not sending?**
- Enable 2-Step Verification in Gmail
- Generate App Password (not your regular password)
- Update MAIL_PASSWORD in .env

**Module not found?**
```powershell
pip install -r requirements.txt
```

**Can't login after migration?**
- Passwords are now hashed
- Use existing credentials (they work)
- Or create new account

## Payment Methods (Simplified)

This implementation includes a **simplified payment gateway**:
- **UPI** - Mock UPI interface
- **Card** - Simplified card form
- **Wallet** - Wallet selection

For production, integrate real payment gateways:
- Razorpay (India)
- Stripe (International)
- Paytm Payment Gateway
- PayU

## Next Steps

1. Configure real email server
2. Integrate real payment gateway
3. Deploy to production server
4. Set up MongoDB Atlas (cloud database)

## Support

For detailed documentation, see: `SETUP_GUIDE.md`

## What Changed?

**Old System:**
- ❌ JSON file storage
- ❌ Plain text passwords
- ❌ No email verification
- ❌ Basic user management
- ❌ No payment processing
- ❌ No invoices

**New System:**
- ✅ MongoDB database
- ✅ Bcrypt password hashing
- ✅ Email OTP verification
- ✅ Full profile management
- ✅ Payment gateway (UPI/Card/Wallet)
- ✅ PDF invoice generation

Enjoy your upgraded car rental system! 🚗
