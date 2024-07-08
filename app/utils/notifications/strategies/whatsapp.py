from twilio.rest import Client
from app.config.settings import settings
from app.utils.notifications.strategies.base import NotificationStrategy

class WhatsAppStrategy(NotificationStrategy):
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send(self, to: str, message: str):
        self.client.messages.create(
            body=message,
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to}"
        )