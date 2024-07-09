from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.reminder_repository import ReminderRepository
from app.repositories.user_repository import UserRepository
from app.repositories.course_repository import CourseRepository
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.scheduler_service import SchedulerService

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.course_repo = CourseRepository(db)
        self.reminder_repo = ReminderRepository(db)
        self.scheduler_service = SchedulerService(db)


    async def create_user(self, user: UserCreate) -> User:
        db_user = await self.user_repo.get_by_code(user.code)
        if not db_user:
            db_user = await self.user_repo.create(user)
        
        user_course = await self.course_repo.get_user_course(db_user.id, user.course_id)
        
        if user_course:
            raise ValueError("The user it's already registered")
        
        _ = await self.course_repo.register_user(db_user.id, user.course_id)

        reminders = await self.reminder_repo.get_all_by_course(user.course_id)
        for reminder in reminders:
            await self.scheduler_service.schedule_reminder(db_user.id, reminder)
            
        return User.model_validate(db_user, from_attributes=True)

    async def get_user(self, user_id: int) -> User:
        db_user = await self.user_repo.get(user_id)
        return User.model_validate(db_user, from_attributes=True)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        db_user = await self.user_repo.get(user_id)
        if db_user is None:
            raise ValueError("User not found")
        return await self.user_repo.update(db_user, user_update)

    async def delete_user(self, user_id: int) -> User:
        db_user = await self.user_repo.get(user_id)
        if db_user is None:
            raise ValueError("User not found")
        return await self.user_repo.delete(user_id)
