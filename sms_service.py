from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")

client = Client(account_sid, auth_token)

def send_sms(water):
    message = f"""
FLOOD ALERT
Water Level: {water} cm
Risk: HIGH
Action: Evacuate immediately
"""
    client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_NUMBER"),
        to=os.getenv("TARGET_NUMBER")
    )