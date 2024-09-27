# users/views.py
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from . import services


@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            # Validate all required fields
            required_fields = ['email', 'name', 'username', 'password']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)

            email = data['email']
            name = data['name']
            username = data['username']
            password = data['password']
            role = data.get('role', 'USER')  # Get role from data or default to USER
            
            user = services.register_user(email, name, username, password, role)
            return JsonResponse({'message': 'User registered successfully', 'user_id': str(user['_id'])}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        except services.UserAlreadyExists:
            return JsonResponse({'error': 'Email or username already exists'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Registration failed', 'details': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            
            # Call the service to authenticate the user
            tokens = services.authenticate_user(email, password)
            
            return JsonResponse({'access_token': tokens['access_token'], 'refresh_token': tokens['refresh_token']}, status=200)
        except KeyError:
            return JsonResponse({'error': 'Missing email or password'}, status=400)
        except services.AuthenticationFailed:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)
        except Exception as e:
            return JsonResponse({'error': 'Login failed', 'details': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutUserView(View):
    def post(self, request):
        return JsonResponse({'message': 'Logout successful. Please delete tokens on client-side.'}, status=200)
