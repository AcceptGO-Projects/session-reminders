from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.course import CourseCreate, CourseUpdate, Course
from app.services.course_service import CourseService
from app.config.data_source import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=Course, summary="Create a new course", description="Create a new course in the system.")
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    course_service = CourseService(db)
    return await course_service.create_course(course)

@router.get("/{course_id}", response_model=Course, summary="Get a course", description="Retrieve a course by its ID.")
async def read_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course_service = CourseService(db)
    return await course_service.get_course(course_id)

@router.get("/", response_model=List[Course], summary="Get all courses", description="Retrieve all courses.")
async def read_courses( db: AsyncSession = Depends(get_db)):
    course_service = CourseService(db)
    return await course_service.get_courses()

@router.put("/{course_id}", response_model=Course, summary="Update a course", description="Update a course's information.")
async def update_course(course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db)):
    course_service = CourseService(db)
    try:
        return await course_service.update_course(course_id, course)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{course_id}", response_model=Course, summary="Delete a course", description="Delete a course by its ID.")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course_service = CourseService(db)
    try:
        return await course_service.delete_course(course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))