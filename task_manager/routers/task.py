from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from task_manager.database import get_db
from task_manager.routers.auth import get_current_user
from task_manager.schemas import TaskCreate, TaskUpdateSchema, TaskResponse
from task_manager.crud import create_task, get_tasks, update_task, delete_task
from typing import Optional

router = APIRouter()

# ✅ 讀取任務列表 (可根據 status 篩選)
@router.get("/", response_model=list[TaskResponse])
def read_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    status: Optional[str] = None
):
    tasks = get_tasks(db, user_id=current_user.id, status=status)  # ✅ 修正 user_id
    return tasks

# ✅ 新增任務
@router.post("/")
def create_new_task(
    task: TaskCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if task.due_date:
        try:
            task.due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式錯誤，請使用 YYYY-MM-DD")

    new_task = create_task(
        db, 
        user_id=current_user.id,  # ✅ 修正 user_id
        title=task.title, 
        description=task.description, 
        due_date=task.due_date, 
        priority=task.priority
    )
    return {"message": "任務新增成功", "task": new_task}

# ✅ 更新任務
@router.put("/{task_id}")
def update_existing_task(
    task_id: int,
    task_update: TaskUpdateSchema,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_task = update_task(db, task_id, current_user.id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="任務不存在或無權限修改")
    return {"message": "任務更新成功", "task": updated_task}

# ✅ 刪除任務
@router.delete("/{task_id}")
def delete_existing_task(
    task_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = delete_task(db, task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="任務不存在或無權限刪除")
    return {"message": "任務刪除成功"}