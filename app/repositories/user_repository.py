from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.future import select

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, user: UserCreate):
        db_user = User(**user.dict())
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update(self, db_user: User, user_update: UserUpdate):
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete(self, user_id: int):
        db_user = await self.get(user_id)
        if db_user:
            await self.db.delete(db_user)
            await self.db.commit()
        return db_user
    
    async def get_users_by_course(self, course_id: int):
        result = await self.db.execute(select(User).join(User.courses).where(User.courses.any(id=course_id)))
        return result.scalars().all()