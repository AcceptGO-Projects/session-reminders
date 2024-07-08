from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.reminder import Reminder
from app.utils.notifications.notification_manager import NotificationManager, NotificationType
from app.repositories.user_repository import UserRepository
from app.repositories.reminder_repository import ReminderRepository

scheduler = AsyncIOScheduler()

class SchedulerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notification_manager = NotificationManager()
        self.user_repository = UserRepository(db)
        self.reminder_repository = ReminderRepository(db)

    async def send_reminder(self, user_id: int, reminder_message: str):
        user = await self.user_repository.get(user_id)
        if user and user.phone:
            await self.notification_manager.send_notification(NotificationType.WHATSAPP, user.phone, reminder_message)

    async def schedule_reminder(self, user_id: int, reminder: Reminder):
        reminder_time = reminder.due_date
        scheduler.add_job(self.send_reminder, DateTrigger(run_date=reminder_time), args=[user_id, reminder.message])

    async def schedule_reminder_for_course(self, course_id: int, reminder: Reminder):
        users = await self.user_repository.get_users_by_course(course_id)
        for user in users:
            await self.schedule_reminder(user.id, reminder)

    async def reschedule_reminder(self, reminder: Reminder):
        scheduler.remove_job(str(reminder.id))
        await self.schedule_reminder_for_course(reminder.course_id, reminder)

if not scheduler.running:
    scheduler.start()
