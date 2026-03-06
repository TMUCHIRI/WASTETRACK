import africastalking
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Africa's Talking
# Monkey-patch requests specifically for the AT sandbox domain to resolve [SSL: WRONG_VERSION_NUMBER]
# which is a known issue with the sandbox SSL configuration on some modern Python/Windows environments.
import requests
from functools import wraps

original_request = requests.Session.request

@wraps(original_request)
def patched_request(self, method, url, *args, **kwargs):
    if url and "api.sandbox.africastalking.com" in url:
        kwargs['verify'] = False
        # Suppress insecure request warnings for sandbox only
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return original_request(self, method, url, *args, **kwargs)

requests.Session.request = patched_request

africastalking.initialize(settings.AT_USERNAME.strip(), settings.AT_API_KEY.strip())


sms = africastalking.SMS

def send_sms(phone_number, message):
    """
    Sends an SMS using Africa's Talking.
    """
    try:
        # sender_id is optional, usually needs to be registered with AT
        # Treat empty string as None to avoid 'InvalidSenderId' errors
        sender_id = settings.AT_SENDER_ID or None
        
        response = sms.send(message, [phone_number], sender_id)

        logger.info(f"SMS response: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
        # In a real app, you might want to raise an exception or handle this gracefully
        return None
