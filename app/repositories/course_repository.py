from sqlalchemy.ext.asyncio import AsyncSession
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from sqlalchemy.future import select

class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, course_id: int):
        result = await self.db.execute(select(Course).where(Course.id == course_id))
        course = result.scalars().first()
        return course

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(select(Course).offset(skip).limit(limit))
        courses = result.scalars().all()
        return courses

    async def create(self, course: CourseCreate):
        db_course = Course(**course.model_dump())
        self.db.add(db_course)
        await self.db.commit()
        await self.db.refresh(db_course)
        return db_course

    async def update(self, db_course: Course, course_update: CourseUpdate):
        update_data = course_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_course, key, value)
        await self.db.commit()
        await self.db.refresh(db_course)
        return db_course

    async def delete(self, course_id: int):
        db_course = await self.get(course_id)
        if db_course:
            await self.db.delete(db_course)
            await self.db.commit()
        return db_course
