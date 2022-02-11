from twilio.rest import Client
from os import environ
from dotenv import load_dotenv

class SMSService:
    def __init__(self):
        load_dotenv()
        self.phone_number = "+18477707025"
        self.client = Client(environ['TWILIO_ACCOUNT_SID'], environ['TWILIO_AUTH_TOKEN'])

    def send_message(self, message):
        message = self.client.messages.create(
            to=self.phone_number,
            from_="+18126252952",
            body=message)

        print("Message sent with ID: {}".format(message.sid))
