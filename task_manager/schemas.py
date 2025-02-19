from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# ✅ 定義任務的請求模型 (用於 POST /tasks/)
class TaskCreate(BaseModel):
    title: str = Field(..., example="完成 FastAPI 研究")  
    description: Optional[str] = Field(None, example="深入測試 FastAPI 任務管理")
    due_date: Optional[str] = Field(None, example="2025-02-10")  
    priority: Literal["高", "中", "低"] = "中"  # ✅ 直接設定預設值，不用 Field

# ✅ 用戶註冊 Schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # ✅ 密碼不能直接存入，需要雜湊處理

# ✅ 用戶回應 Schema（不返回密碼）
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # ✅ 這行很重要，否則 FastAPI 無法處理 SQLAlchemy ORM 對象

# ✅ 任務回應 Schema
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[str]
    priority: str
    completed: bool

    class Config:
        from_attributes = True  # ✅ 這行同樣適用於 ORM 物件

# ✅ Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

# ✅ 更新任務 Schema
class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None