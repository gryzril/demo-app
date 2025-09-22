from sqlalchemy.orm import Session
from app import models
from fastapi import HTTPException

def create_task(db: Session, user_id: int, *, title: str, description: str | None, status: models.Status, due_date, label_ids: list[int]):
    t = models.Task(user_id=user_id, title=title, description=description, status=status, due_date=due_date)
    if label_ids:
        t.labels = db.query(models.Label).filter(models.Label.id.in_(label_ids)).all()
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

def get_task_by_id(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def get_all_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def delete_task_by_id(db: Session, task_id: int) -> None:
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()