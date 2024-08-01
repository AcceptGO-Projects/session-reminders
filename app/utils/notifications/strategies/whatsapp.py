import json
import boto3
from starlette.concurrency import run_in_threadpool

from app.config.settings import settings
from app.utils.notifications.strategies.base import NotificationStrategy

class WhatsAppStrategy(NotificationStrategy):
    def __init__(self):
        self.client = boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self.topic_arn = settings.AWS_SNS_TOPIC_ARN

    async def send(self, to: str, message: str, message_variables: dict):
        payload = {"to": to, "message": message, "message_variables": message_variables}
        response = await run_in_threadpool(
            self.client.publish, TopicArn=self.topic_arn, Message=json.dumps(payload)
        )
        return response