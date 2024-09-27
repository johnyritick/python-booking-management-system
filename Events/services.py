# events/services.py
from .models import Event
from Users.utils import send_email  # Ensure to import the send_email function

class EventService:
    @staticmethod
    def create_event(manager_id, title, description, date, time, location_id, available_tickets, payment_options):
        # Create a new event
        event = Event(
            manager_id=manager_id,
            title=title,
            description=description,
            date=date,
            time=time,
            location_id=location_id,
            available_tickets=available_tickets,
            payment_options=payment_options
        )
        event_record = event.save()

        # Send event creation notification email
        subject = "Event Creation Confirmation"
        message = f"Hello,\n\nYour event '{title}' has been created successfully!"
        manager_email = manager_id  # Assuming manager_id is the user's email; adjust as necessary
        send_email(subject, message, [manager_email])  # Send email to the event manager

        return event_record

    @staticmethod
    def filter_events(location_id=None, date=None, category=None):
        # Filter events based on the provided filters
        return Event.filter_events(location_id, date, category)
