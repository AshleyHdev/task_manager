from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from .schemas import User

# 定義 OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# 加密密碼的上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 模擬用戶數據庫
fake_users_db = {
    "帳號": {
        "id": 1,  # 用戶 ID
        "username": "帳號",
        "email": "帳號@example.com",
        "hashed_password": pwd_context.hash("密碼"),  # ✅ 初始化時生成一次，存入數據庫
    }
}

# JWT 設定
SECRET_KEY = "a_strong_random_secret_key_for_your_app"  # ✅ 更改為隨機且安全的密鑰
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    to_encode.update({"exp": expire, "sub": data["sub"]})  # 確保 sub 正確寫入
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

    # 返回包含完整用戶信息的對象
    return User(id=user["id"], username=user["username"], email=user["email"])
