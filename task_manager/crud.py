from sqlalchemy.orm import Session
from .database import Task

def create_task(db: Session, title: str, description: str, due_date, priority: str):
    task = Task(title=title, description=description, due_date=due_date, priority=priority)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session):
    return db.query(Task).all()

def update_task_status(db: Session, task_id: int, completed: bool):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = completed
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task