from sqlalchemy.orm import Session
from app.models import User
from app.db import SessionLocal
from sqlalchemy.exc import IntegrityError

# Function to create a user
def create_user(db: Session, email: str, password_hash: str, role: str):
    try:
        db_user = User(email=email, password_hash=password_hash, role=role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("A user with this email already exists")

# Function to get a user by ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Function to get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Function to get all users
def get_all_users(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()
