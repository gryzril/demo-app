from __future__ import annotations

# Types for python
from typing import List
import enum

from datetime import datetime

# SqlAlchemy for database schema creation
from sqlalchemy import String, Text, DateTime, Enum, ForeignKey, UniqueConstraint

# SqlAlchemy for object relational mapping
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


### Class Enums ###

# User Role
class Role(str, enum.Enum):
    user = "user"
    admin = "admin"
    
# Status
class Status(str, enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"
    

### Table Mappings ###

class User(Base):
    # decorate table names
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)                                                       # Primary Key (Id)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)                                # One email per user
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user)                                       # Assign user
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())                        
    
    # back_populates
    # cascade: all, delete-orphan. Delete relationship items when user is deleted
    tasks: Mapped[List["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")

# Unique Labels
class Label(Base):
    __tablename__ = "labels"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)

# Tasks
class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)            # Foreign Key (users.id)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text())                                                 # Optional desc
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.todo, index=True)                   # Enum statuses
    due_date: Mapped[datetime | None]
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    user: Mapped["User"] = relationship(back_populates="tasks")
    labels: Mapped[List["Label"]] = relationship(
        secondary="task_labels", lazy="joined"
    )
    
# Many Task to Many Label
class TaskLabel(Base):
    __tablename__ = "task_labels"
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)  
    label_id: Mapped[int] = mapped_column(ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True)

    # Constrain task + label uniqueness
    __table_args__ = (UniqueConstraint("task_id", "label_id", name="uq_task_label"),)