from flask_mail import Mail, Message
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import mongodb
import random
import os
from datetime import datetime

class EmailService:
    def __init__(self, app):
        self.mail = Mail(app)
    
    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def send_otp(self, email, username):
        """Send OTP to user's email"""
        otp = self.generate_otp()
        
        # Store OTP in database with expiry
        mongodb.otps.insert_one({
            'email': email,
            'otp': otp,
            'created_at': datetime.utcnow(),
            'verified': False
        })
        
        # Send email
        try:
            msg = Message(
                subject='Car Rental - Email Verification OTP',
                recipients=[email],
                body=f'''
Hello {username},

Your OTP for email verification is: {otp}

This OTP is valid for 10 minutes.

If you did not request this, please ignore this email.

Best regards,
Car Rental Team
                '''
            )
            self.mail.send(msg)
            return {'success': True, 'message': 'OTP sent successfully'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to send OTP: {str(e)}'}
    
    def verify_otp(self, email, otp):
        """Verify OTP"""
        otp_record = mongodb.otps.find_one({
            'email': email,
            'otp': otp,
            'verified': False
        })
        
        if not otp_record:
            return {'success': False, 'message': 'Invalid or expired OTP'}
        
        # Mark as verified
        mongodb.otps.update_one(
            {'_id': otp_record['_id']},
            {'$set': {'verified': True}}
        )
        
        # Update user email verification status
        mongodb.users.update_one(
            {'email': email},
            {'$set': {'email_verified': True}}
        )
        
        return {'success': True, 'message': 'Email verified successfully'}
    
    def send_booking_confirmation(self, email, booking_details):
        """Send booking confirmation email"""
        try:
            msg = Message(
                subject='Car Rental - Booking Confirmation',
                recipients=[email],
                body=f'''
Dear Customer,

Your booking has been confirmed!

Booking ID: {booking_details['booking_id']}
Car: {booking_details['car_make']} {booking_details['car_model']}
Start Date: {booking_details['start_date']}
End Date: {booking_details['end_date']}
Total Amount: ₹{booking_details['total_price']}

Payment Status: {booking_details['payment_status']}

Thank you for choosing our service!

Best regards,
Car Rental Team
                '''
            )
            self.mail.send(msg)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def send_invoice(self, email, invoice_path):
        """Send invoice as email attachment"""
        try:
            msg = Message(
                subject='Car Rental - Invoice',
                recipients=[email],
                body='Please find your invoice attached.'
            )
            
            if invoice_path and os.path.exists(invoice_path):
                with open(invoice_path, 'rb') as f:
                    msg.attach(
                        filename=os.path.basename(invoice_path),
                        content_type='application/pdf',
                        data=f.read()
                    )
            
            self.mail.send(msg)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}

def send_email(app, to_email, subject, html_body, attachment_path=None):
    """Standalone function to send email with optional attachment"""
    from flask_mail import Mail, Message
    import os
    
    try:
        with app.app_context():
            mail = Mail(app)
            msg = Message(
                subject=subject,
                recipients=[to_email],
                html=html_body
            )
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    msg.attach(
                        filename=os.path.basename(attachment_path),
                        content_type='application/pdf',
                        data=f.read()
                    )
            
            mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
        try:
            msg = Message(
                subject='Car Rental - Invoice',
                recipients=[email],
                body='Please find your invoice attached.'
            )
            with open(invoice_path, 'rb') as f:
                msg.attach('invoice.pdf', 'application/pdf', f.read())
            self.mail.send(msg)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
