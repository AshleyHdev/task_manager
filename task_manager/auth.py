from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from .schemas import User

# ✅ 載入 .env 環境變數
load_dotenv()

# ✅ 從 .env 讀取 SECRET_KEY 和 設定
SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ✅ 讀取 .env 內的用戶資訊
USER_USERNAME = os.getenv("USER_USERNAME", "default_user")
USER_EMAIL = os.getenv("USER_EMAIL", "hidden@example.com")
USER_PASSWORD_HASH = os.getenv("USER_PASSWORD_HASH", "")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 模擬用戶數據庫（改為讀取 .env）
fake_users_db = {
    os.getenv("FAKE_USERNAME", "default_user"): {
        "id": 1,
        "username": os.getenv("FAKE_USERNAME", "default_user"),
        "email": os.getenv("FAKE_EMAIL", "hidden@example.com"),
        "hashed_password": pwd_context.hash(os.getenv("FAKE_PASSWORD", "default_password")),
    }
}
print(f"🔑 Hashed Password: {fake_users_db[os.getenv('FAKE_USERNAME')]['hashed_password']}")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證使用者密碼"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    """驗證用戶憑據"""
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user  # ✅ 返回完整用戶信息

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """生成 JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "sub": data["sub"]})  # ✅ 確保 sub 正確寫入
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """解析 Token 並獲取當前用戶"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="無效的 Token 或未授權"
    )
    try:
        # 解碼 Token 並提取用戶名
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # 獲取用戶名
        if username is None:
            raise credentials_exception
    except JWTError as e:
        # 打印詳細錯誤信息
        print(f"JWT 解碼錯誤: {e}")
        raise credentials_exception

    # 查詢用戶數據庫
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception

    # ✅ 返回包含完整用戶信息的對象
    return User(id=user["id"], username=user["username"], email=user["email"])