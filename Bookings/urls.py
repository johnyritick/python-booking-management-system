# bookings/urls.py
from django.urls import path
from .views import BookTicketView, UserBookingsView, CancelBookingView

urlpatterns = [
    path('book-ticket/', BookTicketView.as_view(), name='book_ticket'),
    path('my-bookings/', UserBookingsView.as_view(), name='user_bookings'),
    path('cancel-booking/<str:booking_id>/', CancelBookingView.as_view(), name='cancel_booking'),
]
