# user_profile/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    MyTokenObtainPairSerializer,
    ChangePasswordSerializer,
)

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)

        email = data.get('email')
        phone_number = data.get('phone_number')
        username = data.get('username')

        # Check if a user with the given username exists
        if User.objects.filter(username=username, is_email_verified=True).exists():
            return Response({'detail': 'A user with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with the given email exists
        if User.objects.filter(email=email, is_email_verified=True).exists():
            return Response({'detail': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with the given phone number exists
        if User.objects.filter(phone_number=phone_number, is_email_verified=True).exists():
            return Response({'detail': 'A user with this phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and create the user if the data is valid
        if serializer.is_valid():
            print('\nCreating user...')
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                phone_number=phone_number,
                password=data.get('password'),
            )

            print('\nUser created! Verify your email.')
            if user.is_email_verified:
                return Response({'detail': 'User already exists. Please login.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'User created. Please verify your email.'}, status=status.HTTP_201_CREATED)
        else:
            print('Error creating user.')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)


class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class GetAllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()  
        serializer = UserProfileSerializer(users, many=True)  
        return Response(serializer.data)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Verify the old password
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
