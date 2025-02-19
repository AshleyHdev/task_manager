📝 Task Manager API 🚀

這是一個基於 **FastAPI** 的任務管理系統，提供使用者認證、JWT 授權、任務 CRUD 操作，適用於任何需要 **管理待辦事項** 的應用場景。

![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688?logo=fastapi&style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.35.5-003B57?logo=sqlite)
![JWT](https://img.shields.io/badge/JWT-Authorization-yellow)

---

## **📌 功能特色**
✅ **使用者註冊 & 登入**  
✅ **JWT Token 身分驗證**  
✅ **任務 CRUD (創建、讀取、更新、刪除)**  
✅ **Swagger 自動 API 文件**  
✅ **支援 SQLite 儲存數據**  
✅ **支援 CORS (允許跨來源請求)**  

---

## **📖 API 文件**
啟動伺服器後，您可以訪問 API 文件：
📌 **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
📌 **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## **💡 安裝與使用**
### **1️⃣ 安裝環境**
確保您已經安裝 **Python 3.10**，然後執行：
```bash
git clone https://github.com/AshleyHdev/task_manager.git
cd task_manager
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
pip install -r requirements.txt

2️⃣ 設定環境變數

在 .env 檔案中設定：

SECRET_KEY="your_secret_key"
ACCESS_TOKEN_EXPIRE_MINUTES=30

3️⃣ 初始化資料庫

alembic upgrade head

4️⃣ 啟動伺服器

uvicorn task_manager.main:app --reload

伺服器啟動後，您可以訪問 http://127.0.0.1:8000/ 🎉

🛠 技術細節
 • FastAPI - 提供高效能 API 框架
 • SQLite - 簡單且輕量級的資料庫
 • JWT (JSON Web Token) - 提供使用者身份驗證
 • Pydantic - 確保數據驗證安全
 • Alembic - 資料庫遷移工具
 • CORS Middleware - 允許前端跨來源請求

🔑 API 認證

本 API 使用 OAuth2 + JWT Token，請先透過 /auth/token 取得 access_token，再將其附加於 API 請求標頭。

取得 Token

curl -X POST "http://127.0.0.1:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=你的帳號&password=你的密碼"

成功回傳：

{
  "access_token": "your_generated_token",
  "token_type": "bearer"
}

驗證 Token

在 API 測試工具中 加上 Header：

Authorization: Bearer your_generated_token

🔧 開發測試

測試用戶

帳號 密碼
test_user 123456

API 測試範例

🔹 創建新任務

curl -X POST "http://127.0.0.1:8000/tasks/" \
     -H "Authorization: Bearer your_generated_token" \
     -H "Content-Type: application/json" \
     -d '{
            "title": "學習 FastAPI",
            "description": "了解 FastAPI 的基本概念",
            "due_date": "2025-02-20",
            "priority": "高"
        }'

🔹 取得所有任務

curl -X GET "http://127.0.0.1:8000/tasks/" \
     -H "Authorization: Bearer your_generated_token"

💙 貢獻方式

歡迎 Fork & PR：
 1. Fork 本專案
 2. 創建新分支 (git checkout -b feature-branch)
 3. 提交修改 (git commit -m "✨ 新增功能")
 4. 推送分支 (git push origin feature-branch)
 5. 發送 PR 🚀

📜 版權聲明

本專案遵循 MIT License，自由使用與修改。
作者：@AshleyH.dev 🎨
