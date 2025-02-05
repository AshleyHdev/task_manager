from sqlalchemy.orm import Session
from .models import Task

def create_task(db: Session, user_id: int, title: str, description: str, due_date, priority: str):
    task = Task(user_id=user_id, title=title, description=description, due_date=due_date, priority=priority)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, user_id: int, status: str = None):
    query = db.query(Task).filter(Task.user_id == user_id)
    if status:
        query = query.filter(Task.status == status)
    return query.all()

def update_task_status(db: Session, task_id: int, user_id: int, completed: bool):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        task.completed = completed
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task