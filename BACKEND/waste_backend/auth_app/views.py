from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import (
    RegisterSerializer, LoginSerializer, VerifyOTPSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    UserSerializer, UserRoleUpdateSerializer, FCMTokenSerializer
)
from rest_framework import generics, permissions
from reports.permissions import IsAdmin
from .notifications import send_push_notification


from .utils import send_otp, verify_otp_logic
from django.utils import timezone
from datetime import timedelta
import random
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .models import CustomUser

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone': user.phone
                },
                'token': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            password = serializer.validated_data['password']
            
            # Try authenticating
            user = authenticate(request, username=identifier, password=password)
                
            if user:
                # If everything is correct, send OTP for 2FA
                send_otp(user)
                return Response({
                    'success': True,
                    'message': 'OTP sent for 2FA verification.',
                    'requires_2fa': True
                }, status=status.HTTP_200_OK)
                
            return Response({
                'success': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            otp = serializer.validated_data['otp']
            
            user = CustomUser.objects.filter(email=identifier).first() or \
                   CustomUser.objects.filter(phone=identifier).first()
            
            if user and verify_otp_logic(user, otp):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'token': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'phone': user.phone,
                        'role': user.role
                    }
                }, status=status.HTTP_200_OK)
            return Response({'success': False, 'message': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            user = CustomUser.objects.filter(email=identifier).first() or \
                   CustomUser.objects.filter(phone=identifier).first()
            
            if user:
                send_otp(user)
            return Response({
                'success': True,
                'message': 'If an account exists, an OTP has been sent.'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            
            user = CustomUser.objects.filter(email=identifier).first() or \
                   CustomUser.objects.filter(phone=identifier).first()
                   
            if user and verify_otp_logic(user, otp):
                user.set_password(new_password)
                user.save()
                return Response({
                    'success': True,
                    'message': 'Password reset successfully.'
                })
            return Response({'success': False, 'message': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserUpdateRoleView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRoleUpdateSerializer
    permission_classes = [IsAdmin]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response({'error': 'You cannot change your own role.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)

class RegisterFCMTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FCMTokenSerializer(data=request.data)
        if serializer.is_valid():
            from .models import FCMDevice
            FCMDevice.objects.update_or_create(
                user=request.user,
                registration_token=serializer.validated_data['registration_token']
            )
            return Response({'success': True, 'message': 'Token registered.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestNotificationView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        user_id = request.data.get('user_id')
        title = request.data.get('title', 'Test Notification')
        body = request.data.get('body', 'This is a test notification from WasteTrack.')
        
        user = CustomUser.objects.filter(id=user_id).first()
        if user:
            send_push_notification(user, title, body)
            return Response({'success': True, 'message': f'Notification sent to {user.email}'})
        return Response({'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


