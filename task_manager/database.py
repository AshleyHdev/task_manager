from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 設定 SQLite 資料庫位置
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# 建立資料庫引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 設定 Session 連線
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立基礎類別
Base = declarative_base()

def init_db():
    """初始化資料庫，只需運行一次"""
    from .models import User, Task  # ✅ 確保 models.py 內的模型已經載入
    Base.metadata.create_all(bind=engine)  # 建立表格