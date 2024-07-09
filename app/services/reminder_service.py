from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.reminder_repository import ReminderRepository
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from app.models.reminder import Reminder
import pytz

class ReminderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.reminder_repo = ReminderRepository(db)

    async def create_reminder(self, reminder: ReminderCreate) -> Reminder:
        reminder.due_date = reminder.due_date.astimezone(pytz.utc)
        return await self.reminder_repo.create(reminder)

    async def get_reminder(self, reminder_id: int) -> Reminder:
        return await self.reminder_repo.get(reminder_id)

    async def update_reminder(self, reminder_id: int, reminder_update: ReminderUpdate) -> Reminder:
        db_reminder = await self.reminder_repo.get(reminder_id)
        if db_reminder is None:
            raise ValueError("Reminder not found")
        reminder_update.due_date = reminder_update.due_date.astimezone(pytz.utc)
        return await self.reminder_repo.update(db_reminder, reminder_update)

    async def delete_reminder(self, reminder_id: int) -> Reminder:
        return await self.reminder_repo.delete(reminder_id)
