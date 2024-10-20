from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import auth 
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json

# 1. Create user
@csrf_exempt  
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        name = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        if not name or not email or not phone or not password:
            return JsonResponse({'error': 'Missing required fields: username, email, phone, and password'}, status=400)

        try:
            user = CustomUser.objects.create(
                username=name,
                email=email,
                phone=phone,
                password=make_password(password)  # Hash the password before saving to database
            )
            return JsonResponse({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


# User Authentication (Login)
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Missing required fields: username and password'}, status=400)

        # Authenticate user credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff
                }
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


# User Logout
def logout_user(request):
    auth.logout(request)
    return redirect('login_user')