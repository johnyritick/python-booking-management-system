# events/views.py
from django.http import JsonResponse
from django.views import View
import json
from bson import ObjectId
from .services import EventService

class CreateEventView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            manager_id = data['manager_id']
            title = data['title']
            description = data['description']
            date = data['date']
            time = data['time']
            location_id = data['location_id']
            available_tickets = data['available_tickets']
            payment_options = data['payment_options']

            # Create the event using the service layer
            event = EventService.create_event(manager_id, title, description, date, time, location_id, available_tickets, payment_options)

            return JsonResponse({'message': 'Event created successfully', 'event_id': str(event.inserted_id)}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Event creation failed', 'details': str(e)}, status=500)

class EventFilterView(View):
    def get(self, request):
        try:
            location_id = request.GET.get('location_id')
            date = request.GET.get('date')
            category = request.GET.get('category')

            # Call the service to filter events
            events = EventService.filter_events(location_id, date, category)

            return JsonResponse({'events': events}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'Failed to filter events', 'details': str(e)}, status=500)
