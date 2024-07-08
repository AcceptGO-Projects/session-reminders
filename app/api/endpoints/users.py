from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate, User
from app.services.user_service import UserService
from app.config.data_source import get_db

router = APIRouter()

@router.post("/", response_model=User, summary="Create a new user", description="Register a new user and enroll them in a course.")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    try:
        return await user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=User, summary="Get a user", description="Retrieve a user by their ID.")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    db_user = await user_service.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User, summary="Update a user", description="Update a user's information.")
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    try:
        return await user_service.update_user(user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", response_model=User, summary="Delete a user", description="Delete a user by their ID.")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    try:
        return await user_service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
