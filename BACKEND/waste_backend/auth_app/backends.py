from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the user exists by email or phone number
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(phone=username)
            except CustomUser.DoesNotExist:
                return None

        # Check if the password is correct
        if user.check_password(password):
            return user
        return None
