from fastapi import APIRouter
from app.api.endpoints import users, reminders, courses

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
router.include_router(courses.router, prefix="/courses", tags=["courses"])