from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.reminder import Reminder
from datetime import timezone

from app.schemas.user import User
from app.utils.notifications.notification_manager import NotificationManager, NotificationType
from app.repositories.user_repository import UserRepository
from app.repositories.reminder_repository import ReminderRepository
from app.helpers.reminder_factory import map_message_variables

scheduler = AsyncIOScheduler()

class SchedulerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notification_manager = NotificationManager()
        self.user_repository = UserRepository(db)
        self.reminder_repository = ReminderRepository(db)

    async def send_reminder(self, user: User, reminder_message: str):
        message_vars = map_message_variables(user)
        if user:
            await self.notification_manager.send_notification(
                notification_type=NotificationType.WHATSAPP, to=user.phone, message=reminder_message, message_variables=message_vars
            )

    async def schedule_reminder(self, user_id: int, reminder: Reminder):
        db_user = await self.user_repository.get(user_id)
        user = User.model_validate(db_user, from_attributes=True)
        reminder_time = reminder.due_date.replace(tzinfo=timezone.utc)
        print(
            scheduler.add_job(self.send_reminder, DateTrigger(run_date=reminder_time), args=[user, reminder.message])
        )

    async def schedule_reminder_for_course(self, course_id: int, reminder: Reminder):
        users = await self.user_repository.get_users_by_course(course_id)
        for user in users:
            await self.schedule_reminder(user.id, reminder)

    async def reschedule_reminder(self, reminder: Reminder):
        scheduler.remove_job(reminder.id)
        await self.schedule_reminder_for_course(reminder.course_id, reminder)

    async def load_pending_reminders(self):
        reminders = await self.reminder_repository.get_all_pending()
        for reminder in reminders:
            users = await self.user_repository.get_users_by_course(reminder.course_id)
            for user in users:
                await self.schedule_reminder(user.id, reminder)

scheduler.start()
