task_manager 專案能夠展現：
 1. 後端開發能力（FastAPI + SQLAlchemy）
 2. 前端整合能力（HTML + JavaScript）
 3. 專案架構設計
 4. 使用 Git 進行版本控制
 5. 可能的擴展性（未來可加入登入系統、任務提醒等）

# Task Manager
這是一個基於 FastAPI 的任務管理應用，支援：
- 建立、查詢、更新、刪除任務（CRUD）
- 使用 SQLite 作為資料庫
- 提供 REST API，可供前端存取
- 透過 PWA（漸進式網頁應用）支援離線模式

## 安裝方式
1. 克隆專案：

git clone https://github.com/AshleyHdev/task_manager.git
cd task_manager

2. 安裝依賴：

pip install -r requirements.txt

3. 啟動後端：

uvicorn task_manager.main:app –reload

4. 開啟 http://127.0.0.1:8000/docs 測試 API。

🚀 如何開啟你的網頁

專案主要是 動態網站，所以需要：
 1. 後端環境運行（啟動 FastAPI）
 2. 前端載入 API

如果本機想開啟網頁

每次要開啟專案，需要：

cd ~/Desktop/task_manager  # 進入專案資料夾
uvicorn task_manager.main:app --reload  # 啟動 FastAPI 伺服器

然後可以開啟：
 • 後端 API 測試 → http://127.0.0.1:8000/docs
 • 前端頁面 → http://127.0.0.1:8000/tasks_html/
