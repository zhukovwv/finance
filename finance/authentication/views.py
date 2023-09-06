from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from finance.authentication.models import UserProfile
from finance.transactions.models import Balance


class RegisterView(APIView):
    @transaction.atomic
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = User(username=username)
            user.set_password(password)
            user.save()

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                Balance.objects.create(user_profile=user_profile)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
