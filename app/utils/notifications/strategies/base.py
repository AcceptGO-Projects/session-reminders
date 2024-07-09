class NotificationStrategy:
    async def send(self, to: str, message: str):
        raise NotImplementedError