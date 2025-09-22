from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import get_user_by_id, create_user, get_all_users
from app.db import get_db
from sqlalchemy.orm import Session

from fastapi.security import HTTPBearer


from app.schemas import UserBase, UserCreate

router = APIRouter()
security = HTTPBearer()

@router.get("/users/{user_id}", 
            summary="Get User by ID", 
            description="Fetch a user by their unique ID.", 
            tags=["Users"], 
            dependencies=[Depends(security)],
            response_model=UserBase)
async def read_user(userId: int, db: Session = Depends(get_db)):
    """
    Fetch a user by their unique user ID. If the user does not exist, a 404 error is returned.
    """
    user = get_user_by_id(db, userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/", 
            summary="Get All Users", 
            description="Fetch a list of users with pagination support.", 
            tags=["Users"], 
            dependencies=[Depends(security)],
            response_model=List[UserBase])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_all_users(db, skip=skip, limit=limit)
    return users

@router.post("/user/", 
            summary="Create a New User", 
            description="Create a new user with the specified details.", 
            tags=["Users"], 
            dependencies=[Depends(security)],
            response_model=UserBase)  # Response model is UserBase
async def create_user_route(user_create: UserCreate, db: Session = Depends(get_db)): 
    """
    Create a new user with the provided email, password hash, and role.
    """
    try:
        # Pass the Pydantic model values (name, email, password_hash) to the service function
        user = create_user(db, user_create.email, user_create.password_hash, user_create.role)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
