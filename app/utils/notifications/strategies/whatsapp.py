from twilio.rest import Client
from starlette.concurrency import run_in_threadpool

from app.config.settings import settings
from app.utils.notifications.strategies.base import NotificationStrategy

class WhatsAppStrategy(NotificationStrategy):
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    async def send(self, to: str, message: str):
        message_response = await run_in_threadpool(
            self.client.messages.create,
            body=message,
            from_=f'whatsapp:{settings.TWILIO_WHATSAPP_FROM}',
            to=f'whatsapp:{to}',
            messaging_service_sid=settings.TWILIO_MESSAGING_SERVICE_SID
        )
        return message_response