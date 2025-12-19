import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import mongodb
from datetime import datetime
import uuid

class PaymentService:
    PAYMENT_METHODS = {
        'UPI': 'UPI Payment',
        'CARD': 'Credit/Debit Card',
        'WALLET': 'Digital Wallet'
    }
    
    @staticmethod
    def initiate_payment(booking_id, amount, payment_method, user_id):
        """Initiate a payment (simplified implementation)"""
        
        # Validate payment method
        if payment_method not in PaymentService.PAYMENT_METHODS:
            return {'success': False, 'message': 'Invalid payment method'}
        
        # Create payment record
        payment = {
            'id': str(uuid.uuid4()),
            'booking_id': booking_id,
            'user_id': user_id,
            'amount': amount,
            'payment_method': payment_method,
            'status': 'pending',
            'transaction_id': f'TXN{uuid.uuid4().hex[:12].upper()}',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        mongodb.payments.insert_one(payment)
        
        # In a real implementation, you would redirect to payment gateway here
        # For simplicity, we'll return payment details
        return {
            'success': True,
            'message': 'Payment initiated',
            'payment': payment
        }
    
    @staticmethod
    def process_payment(payment_id, payment_details):
        """
        Process payment (simplified - in real implementation, this would 
        handle gateway callback/webhook)
        """
        payment = mongodb.payments.find_one({'id': payment_id})
        
        if not payment:
            return {'success': False, 'message': 'Payment not found'}
        
        # Simulate payment processing
        # In real implementation, verify with payment gateway
        
        # Update payment status
        update_data = {
            'status': 'completed',
            'updated_at': datetime.utcnow()
        }
        
        # Add payment gateway response details if provided
        if 'gateway_response' in payment_details:
            update_data['gateway_response'] = payment_details['gateway_response']
        
        mongodb.payments.update_one(
            {'id': payment_id},
            {'$set': update_data}
        )
        
        # Update booking payment status
        mongodb.bookings.update_one(
            {'id': payment['booking_id']},
            {'$set': {
                'payment_status': 'paid',
                'payment_method': payment['payment_method'],
                'payment_id': payment_id
            }}
        )
        
        return {
            'success': True,
            'message': 'Payment completed successfully',
            'payment': payment
        }
    
    @staticmethod
    def get_payment_by_booking(booking_id):
        """Get payment details for a booking"""
        payment = mongodb.payments.find_one({'booking_id': booking_id})
        
        if payment:
            return {'success': True, 'payment': payment}
        return {'success': False, 'message': 'Payment not found'}
    
    @staticmethod
    def simulate_payment_gateway(payment_method, amount):
        """
        Simulate payment gateway for different methods
        Returns payment page details/mock response
        """
        
        if payment_method == 'UPI':
            return {
                'method': 'UPI',
                'upi_id': 'merchant@upi',
                'amount': amount,
                'qr_code': 'mock_qr_code_data',
                'message': 'Scan QR code or enter UPI ID to pay'
            }
        
        elif payment_method == 'CARD':
            return {
                'method': 'CARD',
                'amount': amount,
                'required_fields': ['card_number', 'expiry', 'cvv', 'name'],
                'message': 'Enter card details to proceed'
            }
        
        elif payment_method == 'WALLET':
            return {
                'method': 'WALLET',
                'amount': amount,
                'available_wallets': ['PayTM', 'PhonePe', 'GooglePay', 'AmazonPay'],
                'message': 'Select wallet to proceed'
            }
        
        return {
            'success': False,
            'message': 'Invalid payment method'
        }
    
    @staticmethod
    def refund_payment(payment_id, reason=''):
        """Process refund for a payment"""
        payment = mongodb.payments.find_one({'id': payment_id})
        
        if not payment:
            return {'success': False, 'message': 'Payment not found'}
        
        if payment['status'] != 'completed':
            return {'success': False, 'message': 'Cannot refund incomplete payment'}
        
        # Create refund record
        refund = {
            'id': str(uuid.uuid4()),
            'payment_id': payment_id,
            'amount': payment['amount'],
            'reason': reason,
            'status': 'processed',
            'created_at': datetime.utcnow()
        }
        
        # In real implementation, process refund through payment gateway
        
        # Update payment status
        mongodb.payments.update_one(
            {'id': payment_id},
            {'$set': {
                'status': 'refunded',
                'refund_details': refund,
                'updated_at': datetime.utcnow()
            }}
        )
        
        return {
            'success': True,
            'message': 'Refund processed successfully',
            'refund': refund
        }
