import sys
sys.stdout.reconfigure(encoding='utf-8')

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from .database import SessionLocal, init_db
from .crud import create_task, get_tasks, update_task_status, delete_task

# 初始化資料庫
init_db()

# 設定 FastAPI 應用並支援中文
app = FastAPI(default_response_class=JSONResponse)


# 設定 templates 資料夾
templates = Jinja2Templates(directory="task_manager/templates")

# 新增 HTML 路由
@app.get("/tasks_html/", response_class=HTMLResponse)
def read_tasks_html(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request})

# 資料庫連線
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 根目錄
@app.get("/")
def read_root():
    return {"message": "API 啟動成功"}

# 查詢所有任務
@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = get_tasks(db)
    return tasks

# 新增任務
@app.post("/tasks/")
def create_new_task(
    title: str,
    description: str = None,
    due_date: str = None,
    priority: str = "中",
    db: Session = Depends(get_db)
):
    if due_date:
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式錯誤，請使用 YYYY-MM-DD")
    if priority not in ["高", "中", "低"]:
        raise HTTPException(status_code=400, detail="優先等級必須為 高、中 或 低")
    task = create_task(db, title, description, due_date, priority)
    return {"message": "任務新增成功", "task": task}

# 更新任務完成狀態
@app.put("/tasks/{task_id}")
def update_task(task_id: int, completed: bool, db: Session = Depends(get_db)):
    task = update_task_status(db, task_id, completed)
    if not task:
        raise HTTPException(status_code=404, detail="找不到任務")
    return {"message": "任務更新成功", "task": task}

# 刪除任務
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="找不到任務")
    return {"message": "任務刪除成功"}