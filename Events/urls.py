# events/urls.py
from django.urls import path
from .views import CreateEventView, EventFilterView

urlpatterns = [
    path('create-event/', CreateEventView.as_view(), name='create_event'),
    path('events/', EventFilterView.as_view(), name='filter_events'),
]
