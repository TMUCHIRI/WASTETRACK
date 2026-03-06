import random
import string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp(user):
    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = timezone.now() + timedelta(minutes=10)
    user.save()
    
    # Real SMS integration using Africa's Talking
    message = f"WasteTrack: Your Verification Code is {otp}. Valid for 10 minutes."
    
    if user.phone:
        from .at_service import send_sms
        send_sms(user.phone, message)
    else:
        # Fallback to console or email if no phone is provided
        print(f"MOCK OTP SENT TO {user.email}: {message}")
    
    return otp


def verify_otp_logic(user, otp):
    if user.otp == otp and user.otp_expiry > timezone.now():
        # Clear OTP after successful use
        user.otp = None
        user.otp_expiry = None
        user.save()
        return True
    return False
