import firebase_admin
from firebase_admin import credentials, messaging
import os
from django.conf import settings

# Initialize Firebase Admin SDK
# In a real app, you would provide paths to your service account key JSON
try:
    if not firebase_admin._apps:
        # Mocking credential for development if file doesn't exist
        cred_path = os.path.join(settings.BASE_DIR, 'firebase-service-account.json')
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            print("Firebase service account not found. Push notifications will be mocked.")
except Exception as e:
    print(f"Error initializing Firebase: {e}")

def send_push_notification(user, title, body, data=None):
    from .models import FCMDevice
    
    devices = FCMDevice.objects.filter(user=user)
    if not devices.exists():
        print(f"No devices found for user {user.email}. Mocking notification: {title} - {body}")
        return
    
    tokens = [d.registration_token for d in devices]
    
    if not firebase_admin._apps:
        print(f"MOCK PUSH SENT to {user.email}: [{title}] {body}")
        return

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        tokens=tokens,
    )
    
    try:
        response = messaging.send_multicast(message)
        print(f'Successfully sent {response.success_count} pushes.')
    except Exception as e:
        print(f"Error sending push: {e}")

def send_sms_notification(user, message):
    """
    Sends an SMS notification to the user using Africa's Talking.
    """
    if user.phone:
        from .at_service import send_sms
        return send_sms(user.phone, message)
    return None

