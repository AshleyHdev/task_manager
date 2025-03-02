📝 Task Manager API 🚀

這是一個基於 **FastAPI** 的任務管理系統，提供使用者認證、JWT 授權、任務 CRUD 操作，適用於任何需要 **管理待辦事項** 的應用場景。

![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688?logo=fastapi&style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.35.5-003B57?logo=sqlite)
![JWT](https://img.shields.io/badge/JWT-Authorization-yellow)

---

### 2️⃣ **Task Manager（文本管理工具）**

這個 **Task Manager** 不只是單純的文本處理工具，它其實可以在 **多個行業中發揮作用**，幫助用戶更高效管理和處理文字內容，例如：

✔ **數位內容創作者**（部落客、編輯、寫手）：  
   - 幫助管理 **文章草稿、標籤分類、自動格式化文字**，減少編輯時間。  
   - 可用於 **AI 生成文本後的整理與清理**，確保內容格式一致。  

✔ **客戶服務 / 企業內部溝通**：  
   - 企業客服團隊可以使用這個工具來統一處理 **FAQ 內容、回覆模板、即時筆記**。  
   - 企業內部使用，可作為一個簡單的 **筆記管理+標籤系統**，提升工作效率。  

✔ **程式開發者 & 技術寫作**：  
   - 可以用來管理 **API 文件、程式碼片段、自動整理技術筆記**，讓開發過程更流暢。  

💡 **總結**：這個工具適合所有 **需要處理大量文字內容** 的人，無論是 **創作者、企業還是開發者**，都可以透過它來提升工作效率！  

---

📌 API 端點

📂 任務管理
| 方法 | 端點 | 描述 |
|------|------|------|
| POST | /tasks/ | 創建新任務 |
| GET | /tasks/ | 取得所有任務 |
| GET | /tasks/{task_id} | 查詢單一任務 |
| PUT | /tasks/{task_id} | 更新任務 |
| DELETE | /tasks/{task_id} | 刪除任務 |

🔑 使用者認證

| 方法 | 端點 | 描述 |
|------|------|------|
| POST | /auth/register | 使用者註冊 |
| POST | /auth/token | 登入 & 獲取 JWT Token |
| GET | /users/me | 取得當前使用者資訊 |
| PUT | /users/update | 更新使用者資訊 |
| DELETE | /users/delete | 刪除帳號（不可逆） |

🔍 查詢與篩選

| 參數 | 類型 | 描述 |
|------|------|------|
| completed | boolean | true 取得已完成任務，false 取得未完成任務
| priority | string | 篩選 高/中/低 優先級任務
| due_date | string (YYYY-MM-DD) | 篩選指定截止日期的任務

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
DATABASE_URL="sqlite:///./tasks.db"

3️⃣ 初始化資料庫

如果是 第一次 使用，請先執行：

alembic init alembic  # 只需執行一次
alembic revision --autogenerate -m "初始化資料庫"
alembic upgrade head

如果已經初始化過資料庫：

alembic upgrade head

4️⃣ 啟動伺服器

uvicorn task_manager.main:app --reload

伺服器啟動後，您可以訪問 http://127.0.0.1:8000/ 🎉

📁**專案目錄結構**
```bash
task_manager/
│── alembic/             # 資料庫遷移工具
│── task_manager/
│   ├── main.py          # FastAPI 入口
│   ├── models.py        # 資料庫模型
│   ├── schemas.py       # Pydantic 數據驗證
│   ├── database.py      # 資料庫連線設定
│   ├── crud.py          # 資料操作函式
│   ├── routers/
│   │   ├── auth.py      # 登入 & 註冊 API
│   │   ├── task.py      # 任務 API
│   │   ├── user.py      # 使用者 API
│   ├── .env             # 環境變數 (請自行創建)
│── requirements.txt     # 依賴套件
│── README.md            # 本文件

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

🔧 API 測試範例

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

🔹 查詢單一任務

curl -X GET "http://127.0.0.1:8000/tasks/1" \
     -H "Authorization: Bearer your_generated_token"

🔹 更新任務

curl -X PUT "http://127.0.0.1:8000/tasks/1" \
     -H "Authorization: Bearer your_generated_token" \
     -H "Content-Type: application/json" \
     -d '{
            "title": "更新後的任務標題",
            "completed": true
        }'

🔹 刪除任務

curl -X DELETE "http://127.0.0.1:8000/tasks/1" \
     -H "Authorization: Bearer your_generated_token"

🔍 錯誤排除 (Debugging Tips)

1️⃣ 遇到 500 Internal Server Error
 • 確保 .env 設定正確，並且有執行 alembic upgrade head
 • 檢查 task_manager/database.py 是否正確連結到 SQLite

2️⃣ 遇到 401 Unauthorized
 • 檢查 Authorization Header 是否有正確帶入 Bearer {token}

3️⃣ 遇到 404 Not Found
 • 確保請求的 task_id 是否存在，使用 GET /tasks/ 先檢查

💙 貢獻方式

歡迎 Fork & PR：
 1. Fork 本專案
 2. 創建新分支 (git checkout -b feature-branch)
 3. 提交修改 (git commit -m "✨ 新增功能")
 4. 推送分支 (git push origin feature-branch)
 5. 發送 PR 🚀

📜 **License**
本專案遵循 **MIT License**，使用者可以自由使用、修改、散佈此程式碼，但需保留原始授權聲明，詳情請見 [LICENSE](./LICENSE) 檔案。
作者：@AshleyH.dev 🎨

---

## **🔹 其他技術專案**
- **未來即將上傳更多作品，敬請期待！🚀**
