import sys
sys.stdout.reconfigure(encoding='utf-8')

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.openapi.utils import get_openapi
from .database import SessionLocal, init_db
from .crud import create_task, get_tasks, update_task_status, delete_task
from .auth import get_current_user, authenticate_user, create_access_token, oauth2_scheme
from .schemas import User, Token, TaskCreate
from .models import Task  # 確保 Task 正確導入

# 初始化資料庫
init_db()

def seed_data(db: Session):
    """插入測試數據"""
    if db.query(Task).count() == 0:
        task = Task(
            user_id=1,
            title="Test Task",
            description="This is a test task",
            completed=False,
            priority="中",
            due_date=datetime.utcnow()
        )
        db.add(task)
        db.commit()
        print("✅ 測試數據已插入")

# 測試數據插入
with SessionLocal() as db:
    seed_data(db)

# 定義 FastAPI 應用
app = FastAPI(default_response_class=JSONResponse)

# 自定義 OpenAPI 配置
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Task Manager API",
        version="1.0.0",
        description="Task Management API with OAuth2",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "API 啟動成功"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks/")
def read_tasks(status: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = get_tasks(db, user_id=current_user.id, status=status)
    return tasks

@app.post("/tasks/")
def create_new_task(
    task: TaskCreate,  # ✅ 使用 Pydantic Model 來接受 Request Body
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if task.due_date is not None:  # ✅ 確保不對 None 進行日期轉換
        try:
            task.due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式錯誤，請使用 YYYY-MM-DD")

    new_task = create_task(
        db, 
        user_id=current_user.id, 
        title=task.title, 
        description=task.description, 
        due_date=task.due_date, 
        priority=task.priority
    )
    return {"message": "任務新增成功", "task": new_task}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, completed: bool, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = update_task_status(db, task_id=task_id, user_id=current_user.id, completed=completed)
    if not task:
        raise HTTPException(status_code=404, detail="找不到任務或無權限修改")
    return {"message": "任務更新成功", "task": task}

@app.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """ 刪除指定 ID 的任務 """
    deleted_task = delete_task(db, task_id=task_id, user_id=current_user.id)  # ✅ 正確使用 delete_task
    
    if not deleted_task:
        raise HTTPException(status_code=404, detail="找不到任務或無權限刪除")
    
    return {"message": "任務刪除成功"}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """使用者登入，獲取 JWT Token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/tasks/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}