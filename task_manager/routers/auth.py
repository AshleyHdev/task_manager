from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from dotenv import load_dotenv
import os

from task_manager.database import get_db
from task_manager.models import User
from task_manager.schemas import Token, UserResponse

# ✅ 加載 .env 配置
load_dotenv()

# ✅ 環境變數設定
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")  # 🚨 確保與 Token 產生時相同
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

router = APIRouter()

# ✅ 密碼加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """創建 JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """驗證使用者帳號密碼"""
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """處理使用者登入，回傳 JWT Token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者名稱或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    print(f"✅ 登入成功！發送 Token: {access_token}")  # 🔥 Debug: 確認 Token 是否正確

    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserResponse:
    """解析 JWT Token，獲取當前使用者資訊"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="無法驗證憑證",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # ✅ **修正 Token 格式，去掉 "Bearer " 前綴**
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]

        print(f"🔹 正在解碼 Token: {token}")  # 🔥 Debug: 看 Token 是否正確

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Token 解碼成功！Payload: {payload}")  # 🔥 Debug: 看 Token 內容

        username: Optional[str] = payload.get("sub")
        if username is None:
            print("❌ Token 沒有 'sub' 欄位！")
            raise credentials_exception
    except JWTError as e:
        print(f"❌ JWT 解碼錯誤: {e}")  # 🔥 Debug: 看解碼錯誤
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        print(f"❌ 資料庫找不到用戶: {username}")  # 🔥 Debug: 看是否找到用戶
        raise credentials_exception

    print(f"✅ 用戶驗證成功！用戶: {user.username}")
    return UserResponse(id=user.id, username=user.username, email=user.email)

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    """獲取當前登入使用者的資訊"""
    return current_user