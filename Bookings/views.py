# bookings/views.py
from django.http import JsonResponse
from django.views import View
import json
from bson import ObjectId
from .services import BookingService

class BookTicketView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data['user_id']
            event_id = data['event_id']
            tickets = data['tickets']

            # Check event availability and book tickets
            booking = BookingService.book_ticket(user_id, event_id, tickets)

            return JsonResponse({'message': 'Ticket booked successfully', 'booking_id': str(booking.inserted_id)}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        except BookingService.EventSoldOut:
            return JsonResponse({'error': 'Event is sold out or does not have enough tickets'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Booking failed', 'details': str(e)}, status=500)

class UserBookingsView(View):
    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            bookings = BookingService.get_user_bookings(user_id)

            return JsonResponse({'bookings': bookings}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'Failed to retrieve bookings', 'details': str(e)}, status=500)

class CancelBookingView(View):
    def post(self, request, booking_id):
        try:
            # Cancel the booking
            BookingService.cancel_booking(booking_id)

            return JsonResponse({'message': 'Booking canceled successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'Cancellation failed', 'details': str(e)}, status=500)
