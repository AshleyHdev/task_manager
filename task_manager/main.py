import sys
sys.stdout.reconfigure(encoding='utf-8')

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from task_manager.database import init_db
from task_manager.routers import auth, task, user

# ✅ 載入 .env 環境變數
load_dotenv()

# ✅ 初始化資料庫
init_db()

# ✅ 創建 FastAPI 應用
app = FastAPI(
    title="Task Manager API",
    description="Task Management API with OAuth2",
    version="1.0.0",
    default_response_class=JSONResponse
)

# ✅ 設定 CORS（避免前端請求 API 受限）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 這裡可以換成你的前端網址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 註冊 routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(user.router, prefix="/users", tags=["Users"])

# ✅ **自訂 OpenAPI，確保 Authorize (🔓) 按鈕顯示**
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # ✅ **確保 Swagger UI 有 OAuth2 驗證**
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

    app.openapi_schema = openapi_schema
    return openapi_schema

# ✅ **套用 `custom_openapi()`**
app.openapi = custom_openapi

# ✅ **API 啟動成功測試**
@app.get("/")
def read_root():
    return {"message": "API 啟動成功"}