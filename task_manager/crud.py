from sqlalchemy.orm import Session
from .models import Task
from .schemas import TaskCreate, TaskUpdateSchema
from typing import Optional, List

# ✅ 創建新任務
def create_task(db: Session, user_id: int, title: str, description: Optional[str], due_date: Optional[str], priority: str):
    new_task = Task(
        user_id=user_id,
        title=title,
        description=description,
        due_date=due_date,  # 這裡仍存入 datetime 格式，避免 DB 操作錯誤
        priority=priority
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# ✅ 讀取任務，並確保 due_date 變成 YYYY-MM-DD 格式的 str
def get_tasks(db: Session, user_id: Optional[int] = None, status: Optional[str] = None) -> List[dict]:
    query = db.query(Task)

    if user_id is not None:
        query = query.filter(Task.user_id == user_id)

    if status:
        query = query.filter(Task.status == status)

    tasks = query.all()

    # ✅ 確保 due_date 是 str
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None,
            "priority": task.priority,
            "status": task.status,
            "completed": task.completed
        }
        for task in tasks
    ]

# ✅ 更新任務
def update_task(db: Session, task_id: int, user_id: int, task_update: TaskUpdateSchema):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    
    if not task:
        return None  # 找不到任務或無權限

    for key, value in task_update.model_dump(exclude_unset=True).items():  # Pydantic v2 需要用 model_dump
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

# ✅ 刪除任務
def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    
    if not task:
        return False  # 找不到任務或無權限

    db.delete(task)
    db.commit()
    return True