from pydantic import BaseModel, Field
from typing import Optional, Literal

# ✅ 定義任務的請求模型 (用於 POST /tasks/)
class TaskCreate(BaseModel):
    title: str = Field(..., example="完成 FastAPI 研究")  # ✅ 確保 title 必填
    description: Optional[str] = Field(None, example="深入測試 FastAPI 任務管理")
    due_date: Optional[str] = Field(None, example="2025-02-10")  # ✅ 使用 str，FastAPI 會解析
    priority: Literal["高", "中", "低"] = Field("中", example="高")  # ✅ 使用 Literal 限定值

# ✅ 用戶 Schema
class User(BaseModel):
    id: int
    username: str
    email: str

# ✅ Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str