from typing import List
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.services.task_service import create_task, delete_task_by_id, get_task_by_id, get_all_tasks
from app.db import get_db
from app.schemas import TaskCreate, TaskBase

router = APIRouter()
security = HTTPBearer()

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", 
             summary="Create a New Task", 
             description="Create a new task with the specified details.", 
             tags=["Tasks"], 
             response_model=TaskBase)  # Use the TaskBase Pydantic model for the response
async def create_task_route(task_create: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task with the provided title, description, status, and due date.
    """
    try:
        task = create_task(db, user_id=1,  # Assuming `user_id` is passed or extracted from context
                           title=task_create.title, 
                           description=task_create.description,
                           status=task_create.status,
                           due_date=task_create.due_date,
                           label_ids=task_create.label_ids)
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}", 
            summary="Get Task by ID", 
            description="Fetch a task by its unique ID.", 
            tags=["Tasks"], 
            response_model=TaskBase)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Fetch a task by its unique task ID. If the task does not exist, a 404 error is returned.
    """
    task = get_task_by_id(db, task_id)  # Call the service layer to fetch the task
    return task

@router.get("", 
            summary="Get All Tasks", 
            description="Fetch a list of tasks with pagination support.", 
            tags=["Tasks"], 
            response_model=List[TaskBase])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetch all tasks from the database with pagination. Use `skip` and `limit` for pagination.
    """
    tasks = get_all_tasks(db, skip=skip, limit=limit)
    return tasks

@router.delete("/{task_id}", 
            summary="Delete Task by ID", 
            description="Delete a task by its unique ID.", 
            tags=["Tasks"], 
            status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Fetch a task by its unique task ID. If the task does not exist, a 404 error is returned.
    """
    delete_task_by_id(db, task_id) 
    return Response(status_code=204)

