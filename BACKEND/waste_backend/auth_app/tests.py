from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_path = '/auth/register/'
        self.login_path = '/auth/login/'
        self.verify_otp_path = '/auth/verify-otp/'
        self.password_reset_path = '/auth/password-reset/'
        self.password_reset_confirm_path = '/auth/password-reset-confirm/'
        
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '+254712345678',
            'password': 'password123',
            'role': 'resident'
        }

    def test_registration_success(self):
        response = self.client.post(self.register_path, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue('token' in response.data)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_login_2fa_flow(self):
        # Register user
        self.client.post(self.register_path, self.user_data, format='json')
        
        # Step 1: Login with password
        login_data = {
            'identifier': 'john@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_path, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['requires_2fa'])
        
        # Step 2: Verify OTP
        user = CustomUser.objects.get(email='john@example.com')
        otp = user.otp
        verify_data = {
            'identifier': 'john@example.com',
            'otp': otp
        }
        verify_response = self.client.post(self.verify_otp_path, verify_data, format='json')
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in verify_response.data)

    def test_password_reset_flow(self):
        # Register user
        self.client.post(self.register_path, self.user_data, format='json')
        
        # Step 1: Request reset
        response = self.client.post(self.password_reset_path, {'identifier': 'john@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Step 2: Confirm reset with OTP
        user = CustomUser.objects.get(email='john@example.com')
        otp = user.otp
        confirm_data = {
            'identifier': 'john@example.com',
            'otp': otp,
            'new_password': 'newpassword123'
        }
        confirm_response = self.client.post(self.password_reset_confirm_path, confirm_data, format='json')
        self.assertEqual(confirm_response.status_code, status.HTTP_200_OK)
        
        # Step 3: Try login with new password
        login_data = {
            'identifier': 'john@example.com',
            'password': 'newpassword123'
        }
        login_response = self.client.post(self.login_path, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertTrue(login_response.data['requires_2fa'])
