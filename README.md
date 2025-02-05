Task Manager API - FastAPI 任務管理系統

這是一個基於 FastAPI 的任務管理 API，實現了 CRUD（Create、Read、Update、Delete） 功能，並支援 OAuth2 JWT 身份驗證，確保只有授權用戶可以存取任務數據。

📌 目錄
 • 🌟 主要功能
 • 🚀 環境需求
 • 🔧 安裝與設定
 • 🖥️ 啟動專案
 • 🔑 身份驗證
 • 📌 API 端點
 • 🛠️ 主要技術
 • 📄 目錄結構
 • 📢 貢獻指南
 • 📜 授權

🌟 主要功能

✅ 使用 FastAPI 提供 RESTful API
✅ 支援 JWT 身份驗證（OAuth2 + JWT Token）
✅ 內建 SQLite 資料庫（可改為 PostgreSQL / MySQL）
✅ 完整的 CRUD 操作：
 • 新增任務
 • 查詢任務
 • 更新任務狀態
 • 刪除任務
✅ Swagger UI（API Docs）：可視化測試 API
✅ pydantic 數據驗證，確保請求數據有效
✅ 異步處理，提升效能

🚀 環境需求

請確保你的系統已安裝以下環境：
 • Python 3.10+
 • pip 22.0+
 • Git
 • SQLite（或其他 SQL 資料庫）

🔧 安裝與設定

1️⃣ 克隆專案

git clone https://github.com/AshleyHdev/task_manager.git
cd task_manager

2️⃣ 建立虛擬環境

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ 安裝相依套件

pip install -r requirements.txt

🖥️ 啟動專案

1️⃣ 初始化資料庫

rm tasks.db  # 刪除舊資料庫（如存在）
python3 -c "from task_manager.database import init_db; init_db()"

2️⃣ 啟動 FastAPI 伺服器

uvicorn task_manager.main:app --reload

啟動後，你可以透過以下方式訪問 API：
 • API 端點測試（Swagger UI）：
👉 http://127.0.0.1:8000/docs
 • 查看 OpenAPI JSON：
👉 http://127.0.0.1:8000/openapi.json

🔑 身份驗證

本專案使用 OAuth2 + JWT 進行身份驗證，步驟如下：

1️⃣ 獲取 Access Token

使用 POST /token 取得 JWT Token：

curl -X 'POST' 'http://127.0.0.1:8000/token' \
-H 'accept: application/json' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'grant_type=password&username=您的帳號&password=*******&scope=&client_id=&client_secret='

🔹 返回結果

{
  "access_token": "your_jwt_token_here",
  "token_type": "bearer"
}

2️⃣ 在 API 請求中加入 Token

當存取受保護的 API 時，請將 Token 加入 Authorization 標頭：

curl -X 'GET' 'http://127.0.0.1:8000/tasks/' \
-H "Authorization: Bearer your_jwt_token_here" \
-H 'accept: application/json'

📌 API 端點

📍 用戶認證

方法 端點 描述
POST /token 取得 JWT Token

📍 任務管理

方法 端點 描述
GET /tasks/ 查詢所有任務
POST /tasks/ 新增任務
PUT /tasks/{task_id}?completed=true 更新任務狀態
DELETE /tasks/{task_id} 刪除任務

📌 詳細 API 文件請參考 http://127.0.0.1:8000/docs

🛠️ 主要技術

技術 用途
FastAPI 構建 API 服務
SQLite 內建資料庫（可換成 PostgreSQL）
SQLAlchemy ORM 操作資料庫
Pydantic 數據驗證
JWT (PyJWT) Token 驗證
Uvicorn 運行 FastAPI 伺服器

📄 目錄結構

task_manager/
│── task_manager/
│   ├── __init__.py
│   ├── main.py          # 主應用程式
│   ├── database.py      # 資料庫初始化
│   ├── models.py        # 資料庫模型
│   ├── schemas.py       # Pydantic 數據模型
│   ├── crud.py          # 資料庫操作函數
│   ├── auth.py          # JWT Token 身份驗證
│   ├── seed_data        # 測試數據
│── requirements.txt     # 相依套件
│── README.md            # 自述文件（本檔案）
