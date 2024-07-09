from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.course_repository import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate, Course

class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repo = CourseRepository(db)

    async def create_course(self, course: CourseCreate) -> Course:
        db_course = await self.course_repo.create(course)
        return Course.model_validate(db_course, from_attributes=True)

    async def get_course(self, course_id: int) -> Course:
        db_course = await self.course_repo.get(course_id)
        if not db_course:
            raise ValueError("Course not found")
        return Course.model_validate(db_course, from_attributes=True)
    
    async def get_courses(self) -> List[Course]:
        db_courses = await self.course_repo.get_all()
        if not db_courses:
            raise ValueError("there are no courses yet")
        return [Course.model_validate(db_course, from_attributes=True) for db_course in db_courses]

    async def update_course(self, course_id: int, course_update: CourseUpdate) -> Course:
        db_course = await self.course_repo.get(course_id)
        if not db_course:
            raise ValueError("Course not found")
        updated_course = await self.course_repo.update(db_course, course_update)
        return Course.model_validate(updated_course, from_attributes=True)

    async def delete_course(self, course_id: int) -> Course:
        db_course = await self.course_repo.get(course_id)
        if not db_course:
            raise ValueError("Course not found")
        deleted_course = await self.course_repo.delete(course_id)
        return Course.model_validate(deleted_course, from_attributes=True)
