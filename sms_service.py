import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(recipient_number, message):
    """
    Send SMS using Twilio
    
    Args:
        recipient_number (str): Phone number to send SMS to (e.g., +8801234567890)
        message (str): Message content
        
    Returns:
        tuple: (success: bool, response: str)
    """
    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        return True, f"SMS sent successfully! ID: {msg.sid}"
    except Exception as e:
        return False, f"Error sending SMS: {str(e)}"

def validate_phone_number(phone_number):
    """
    Validate phone number format
    
    Args:
        phone_number (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Basic validation - should start with + and contain only digits after that
    if not phone_number.startswith('+'):
        return False
    if not phone_number[1:].isdigit():
        return False
    if len(phone_number) < 10:
        return False
    return True
