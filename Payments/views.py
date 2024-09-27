# payment/views.py
from django.http import JsonResponse
from django.views import View
import json
from .services import PaymentService

class MakePaymentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            booking_id = data['booking_id']
            amount = data['amount']

            PaymentService.make_payment(booking_id, amount)

            return JsonResponse({'message': 'Payment processed successfully'}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Payment failed', 'details': str(e)}, status=500)

class RevertPaymentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            booking_id = data['booking_id']

            PaymentService.revert_payment(booking_id)

            return JsonResponse({'message': 'Payment reverted successfully'}, status=200)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Reverting payment failed', 'details': str(e)}, status=500)
