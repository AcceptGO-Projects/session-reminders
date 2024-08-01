from app.utils.notifications.strategies.notification_type import NotificationType
from app.utils.notifications.strategies.whatsapp import WhatsAppStrategy

class NotificationManager:
    def __init__(self):
        self.strategies = {
            NotificationType.WHATSAPP: WhatsAppStrategy(),
        }

    async def send_notification(self, notification_type: NotificationType, to: str, message: str, message_variables: dict):
        strategy = self.strategies.get(notification_type)
        if strategy:
            await strategy.send(to, message, message_variables)
        else:
            raise ValueError("Unsupported notification type")
