from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.reminder import ReminderCreate, ReminderUpdate, Reminder
from app.services.reminder_service import ReminderService
from app.config.data_source import get_db

router = APIRouter()

@router.post("/", response_model=Reminder, summary="Create a new reminder", description="Create a new reminder for a course.")
async def create_reminder(reminder: ReminderCreate, db: AsyncSession = Depends(get_db)):
    reminder_service = ReminderService(db)
    return await reminder_service.create_reminder(reminder)

@router.get("/{reminder_id}", response_model=Reminder, summary="Get a reminder", description="Retrieve a reminder by its ID.")
async def read_reminder(reminder_id: int, db: AsyncSession = Depends(get_db)):
    reminder_service = ReminderService(db)
    db_reminder = await reminder_service.get_reminder(reminder_id)
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return db_reminder

@router.put("/{reminder_id}", response_model=Reminder, summary="Update a reminder", description="Update a reminder's information.")
async def update_reminder(reminder_id: int, reminder: ReminderUpdate, db: AsyncSession = Depends(get_db)):
    reminder_service = ReminderService(db)
    try:
        return await reminder_service.update_reminder(reminder_id, reminder)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{reminder_id}", response_model=Reminder, summary="Delete a reminder", description="Delete a reminder by its ID.")
async def delete_reminder(reminder_id: int, db: AsyncSession = Depends(get_db)):
    reminder_service = ReminderService(db)
    try:
        return await reminder_service.delete_reminder(reminder_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
