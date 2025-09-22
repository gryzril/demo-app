from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class Role(str, Enum):
    user = "user"
    admin = "admin"

class Status(str, Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class UserBase(BaseModel):
    id: int
    email: str
    role: Role
    created_date: datetime

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries

class UserCreate(BaseModel):
    email: str
    password_hash: str
    role: Role = Role.user  # Default role to 'user'

    class Config:
        orm_mode = True 

class TaskBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Status
    due_date: datetime
    labels: List[int]  # List of label IDs associated with the task
    user_id: int

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status
    due_date: datetime
    label_ids: List[int] = []  # List of label IDs to associate with the task

    class Config:
        orm_mode = True

