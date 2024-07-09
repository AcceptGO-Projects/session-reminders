from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from sqlalchemy.future import select
import pytz

class ReminderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, reminder_id: int):
        result = await self.db.execute(select(Reminder).where(Reminder.id == reminder_id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(select(Reminder).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, reminder: ReminderCreate):
        reminder_data = reminder.model_dump()
        reminder_data['due_date'] = reminder_data['due_date'].astimezone(pytz.utc)
        db_reminder = Reminder(**reminder_data)
        self.db.add(db_reminder)
        await self.db.commit()
        await self.db.refresh(db_reminder)
        return db_reminder

    async def update(self, db_reminder: Reminder, reminder_update: ReminderUpdate):
        update_data = reminder_update.model_dump(exclude_unset=True)
        if 'due_date' in update_data:
            update_data['due_date'] = update_data['due_date'].astimezone(pytz.utc)
        for key, value in update_data.items():
            setattr(db_reminder, key, value)
        await self.db.commit()
        await self.db.refresh(db_reminder)
        return db_reminder

    async def delete(self, reminder_id: int):
        db_reminder = await self.get(reminder_id)
        if db_reminder:
            await self.db.delete(db_reminder)
            await self.db.commit()
        return db_reminder
    
    async def get_all_by_course(self,course_id: int):
        result = await self.db.execute(select(Reminder).where(Reminder.course_id == course_id))
        return result.scalars().all()