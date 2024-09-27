# bookings/services.py
from .models import Booking
from Users.models import UserManager
from Users.utils import send_email 

class BookingService:
    class EventSoldOut(Exception):
        pass

    @staticmethod
    def book_ticket(user_id, event_id, tickets):
        # Check if the event has enough available tickets
        if not Booking.check_event_availability(event_id, tickets):
            raise BookingService.EventSoldOut()

        # Update event ticket availability
        Booking.update_event_tickets(event_id, tickets)

        # Create and save a new booking
        booking = Booking(user_id=user_id, event_id=event_id, tickets=tickets)
        booking_record = booking.save()

        # Send booking confirmation email
        subject = "Ticket Booking Confirmation"
        message = f"Hello,\n\nYour booking for event ID {event_id} with {tickets} tickets has been confirmed!"
        send_email(subject, message, [user_id])  # Assuming user_id is the user's email; modify as necessary.

        return booking_record

    @staticmethod
    def get_user_bookings(user_id):
        # Retrieve bookings for the user
        bookings = Booking.find_by_user(user_id)
        return [{'event_id': str(booking['event_id']), 'tickets': booking['tickets'], 'booking_date': booking['booking_date']} for booking in bookings]

    @staticmethod
    def cancel_booking(booking_id):
        # Cancel the booking
        booking = Booking.find_by_id(booking_id)
        if booking:
            # Send cancellation email
            subject = "Booking Cancellation"
            message = f"Hello,\n\nYour booking with ID {booking_id} has been canceled."
            user_email = booking['user_id']  # Assuming you store the user's email in your booking data.
            send_email(subject, message, [user_email])  # Send cancellation email

        Booking.cancel_booking(booking_id)
    
    def get_users_by_event(event_id):
        bookings = Booking.objects.filter(event_id=event_id)
        user_ids = bookings.values_list('user_id', flat=True)
        users = UserManager.objects.filter(id__in=user_ids)
        return users