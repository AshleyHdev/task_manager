from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from task_manager.database import get_db  # ✅ 確保正確導入
from task_manager.schemas import UserCreate, UserResponse
from task_manager.models import User
from task_manager.routers.auth import get_password_hash  # ✅ 確保導入密碼雜湊函式

# ✅ 創建 APIRouter
router = APIRouter()

# ✅ 創建新用戶 API
@router.post("/", response_model=UserResponse)  # ✅ 修正這裡，避免 /users/users/
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """ 創建新用戶 """
    # ✅ 檢查用戶是否已存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="使用者已存在")

    # ✅ 密碼加密後存入資料庫
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user