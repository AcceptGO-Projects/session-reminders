from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.repositories.course_repository import CourseRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.course_repo = CourseRepository(db)

    async def create_user(self, user: UserCreate) -> User:
        db_user = await self.user_repo.get_by_email(user.email)
        if db_user:
            raise ValueError("Email already registered")
        db_course = await self.course_repo.get(user.course_id)
        if db_course is None:
            raise ValueError("Course not found")
        new_user = await self.user_repo.create(user)
        db_course.users.append(new_user)
        await self.db.commit()
        return new_user

    async def get_user(self, user_id: int) -> User:
        return await self.user_repo.get(user_id)

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
