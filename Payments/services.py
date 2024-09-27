# payment/services.py
from .models import Payment
from Bookings.models import Booking

class PaymentService:
    @staticmethod
    def make_payment(booking_id, amount):
        # Simulate payment processing
        # Here you might want to add actual payment processing logic
        payment = Payment(booking_id=booking_id, amount=amount, payment_status='completed')
        payment.save()
        
        # Update booking status to 'confirmed'
        Booking.update_booking_status(booking_id, 'confirmed')  # Ensure this method exists in Booking model

    @staticmethod
    def revert_payment(booking_id):
        # Revert the payment
        # Here you might want to add actual payment reverting logic
        Booking.update_booking_status(booking_id, 'canceled')  # Ensure this method exists in Booking model
