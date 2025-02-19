from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from task_manager.database import get_db
from task_manager.routers.auth import get_current_user
from task_manager.schemas import TaskCreate, TaskUpdateSchema, TaskResponse
from task_manager.crud import create_task, get_tasks
from typing import Optional  # ✅ 確保 Optional 被導入

router = APIRouter()

@router.get("/", response_model=list[TaskResponse])
def read_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    status: Optional[str] = None
):
    tasks = get_tasks(db, user_id=current_user.username, status=status)  # ✅ 正確存取 username
    return tasks

@router.post("/")
def create_new_task(
    task: TaskCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if task.due_date:
        try:
            task.due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()  # ✅ 確保是日期物件
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式錯誤，請使用 YYYY-MM-DD")

    new_task = create_task(
        db, 
        user_id=current_user.username,  # ✅ 使用 .username
        title=task.title, 
        description=task.description, 
        due_date=task.due_date, 
        priority=task.priority
    )
    return {"message": "任務新增成功", "task": new_task}