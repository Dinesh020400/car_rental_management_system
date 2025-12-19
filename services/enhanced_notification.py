from services.email_service import send_email
from services.invoice_service_pro import ProfessionalInvoiceGenerator
import threading
from flask import current_app

class EnhancedNotificationService:
    """Enhanced notification service with merged email and professional invoices"""
    
    @staticmethod
    def send_booking_confirmation_with_invoice(user_email, user_name, booking_data, payment_data, invoice_path):
        """Send combined booking confirmation and invoice in single email"""
        subject = f"Booking Confirmed #{booking_data.get('id', 'N/A')[:8]} - Invoice Attached"
        
        # Calculate arrival estimate
        pickup_datetime = f"{booking_data.get('start_date', '')} {booking_data.get('pickup_time', '')}"
        
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 650px; margin: 0 auto; padding: 20px; background: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .success-badge {{ display: inline-block; background: #10b981; color: white; padding: 8px 20px; border-radius: 20px; margin-top: 15px; font-weight: bold; }}
                .content {{ padding: 30px; background: #f9fafb; }}
                .card {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .card-header {{ font-size: 18px; font-weight: bold; color: #667eea; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
                .info-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb; }}
                .info-label {{ font-weight: 600; color: #6b7280; }}
                .info-value {{ color: #111827; text-align: right; }}
                .total-section {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .total-amount {{ font-size: 32px; font-weight: bold; text-align: center; }}
                .btn {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 10px 5px; }}
                .btn-secondary {{ background: #6b7280; }}
                .checklist {{ background: #fef3c7; padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b; }}
                .checklist-item {{ padding: 8px 0; }}
                .checklist-item:before {{ content: "✓"; color: #10b981; font-weight: bold; margin-right: 10px; }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
                .highlight {{ background: #fef3c7; padding: 2px 6px; border-radius: 3px; font-weight: 600; }}
                .gps-alert {{ background: #dbeafe; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin: 15px 0; }}
                .gps-icon {{ font-size: 24px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Booking Confirmed!</h1>
                    <div class="success-badge">✓ Payment Successful</div>
                </div>
                
                <div class="content">
                    <p style="font-size: 16px; margin-bottom: 25px;">Dear <strong>{user_name}</strong>,</p>
                    
                    <p style="font-size: 15px;">Your booking has been confirmed and payment processed successfully. Your invoice is attached to this email.</p>
                    
                    <!-- Booking Details Card -->
                    <div class="card">
                        <div class="card-header">📋 Booking Details</div>
                        <div class="info-row">
                            <span class="info-label">Booking ID:</span>
                            <span class="info-value">#{booking_data.get('id', 'N/A')[:12]}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Vehicle:</span>
                            <span class="info-value">{booking_data.get('car_brand', '')} {booking_data.get('car_model', 'Vehicle')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Rental Period:</span>
                            <span class="info-value">{booking_data.get('start_date', 'N/A')} to {booking_data.get('end_date', 'N/A')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Duration:</span>
                            <span class="info-value">{booking_data.get('total_days', 0)} days</span>
                        </div>
                    </div>
                    
                    <!-- Pickup Details Card -->
                    <div class="card">
                        <div class="card-header">📍 Pickup & Drop Details</div>
                        <div class="info-row">
                            <span class="info-label">Pickup Location:</span>
                            <span class="info-value">{booking_data.get('pickup_location', 'Not specified')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Pickup Time:</span>
                            <span class="info-value">{booking_data.get('pickup_time', 'N/A')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Drop Location:</span>
                            <span class="info-value">{booking_data.get('drop_location', 'Not specified')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Drop Time:</span>
                            <span class="info-value">{booking_data.get('drop_time', 'N/A')}</span>
                        </div>
                    </div>
                    
                    <!-- Payment Details Card -->
                    <div class="card">
                        <div class="card-header">💳 Payment Information</div>
                        <div class="info-row">
                            <span class="info-label">Payment Method:</span>
                            <span class="info-value">{payment_data.get('method', 'N/A').upper()}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Transaction ID:</span>
                            <span class="info-value">{payment_data.get('transaction_id', 'N/A')[:20]}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Payment Status:</span>
                            <span class="info-value" style="color: #10b981; font-weight: bold;">✓ PAID</span>
                        </div>
                    </div>
                    
                    <!-- Total Amount -->
                    <div class="total-section">
                        <div style="font-size: 14px; margin-bottom: 5px;">Total Amount Paid</div>
                        <div class="total-amount">&#8377;{booking_data.get('total_price', 0):,.2f}</div>
                        <div style="font-size: 12px; margin-top: 5px; opacity: 0.9;">Invoice #{booking_data.get('id', 'N/A')[:8].upper()} attached</div>
                    </div>
                    
                    <!-- Pre-Pickup Checklist -->
                    <div class="checklist">
                        <h3 style="margin-top: 0; color: #92400e;">📝 Pre-Pickup Checklist</h3>
                        <div class="checklist-item">Valid Driving License (Original)</div>
                        <div class="checklist-item">Government ID Proof (Aadhar/PAN/Passport)</div>
                        <div class="checklist-item">Booking Confirmation (This Email or PDF)</div>
                        <div class="checklist-item">Payment Receipt/Transaction Details</div>
                        <div class="checklist-item">Arrive 15 minutes before pickup time</div>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5000/my-bookings" class="btn">
                            📱 View My Bookings
                        </a>
                    </div>
                    
                    <!-- Important Notes -->
                    <div style="background: #fee2e2; padding: 15px; border-radius: 8px; border-left: 4px solid #ef4444; margin: 20px 0;">
                        <strong style="color: #991b1b;">⚠️ Important:</strong>
                        <ul style="margin: 10px 0; padding-left: 20px; color: #7f1d1d;">
                            <li>Late return charges: <span class="highlight">&#8377;500 per hour</span></li>
                            <li>Fuel should be <span class="highlight">refilled before return</span></li>
                            <li>Vehicle inspection will be done at pickup and return</li>
                        </ul>
                    </div>
                    
                    <p style="color: #6b7280; font-size: 14px; margin-top: 25px;">
                        Need help? Contact us at <strong>+91 98765 43210</strong> or reply to this email.
                    </p>
                </div>
                
                <div class="footer">
                    <p style="margin: 5px 0;">Thank you for choosing <strong>Premium Car Rentals</strong>!</p>
                    <p style="margin: 5px 0; font-size: 12px;">This is an automated email. Please do not reply.</p>
                    <p style="margin: 15px 0 5px 0; font-size: 12px;">📧 info@carrentals.com | 📞 +91 98765 43210 | 🌐 www.carrentals.com</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email with invoice attachment in background
        app = current_app._get_current_object()
        thread = threading.Thread(
            target=send_email,
            args=(app, user_email, subject, body, invoice_path)
        )
        thread.start()
        return True
    
    @staticmethod
    def generate_and_send_invoice(booking_data, payment_data, user_data):
        """Generate professional invoice and send combined email"""
        try:
            # Generate invoice
            invoice_gen = ProfessionalInvoiceGenerator()
            invoice_info = invoice_gen.generate_invoice(booking_data, payment_data, user_data)
            
            # Send combined email
            EnhancedNotificationService.send_booking_confirmation_with_invoice(
                user_email=user_data.get('email'),
                user_name=user_data.get('username', 'Customer'),
                booking_data=booking_data,
                payment_data=payment_data,
                invoice_path=invoice_info['filepath']
            )
            
            return True, invoice_info
        except Exception as e:
            print(f"Error generating and sending invoice: {e}")
            return False, None
