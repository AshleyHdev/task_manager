from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from task_manager.database import Base  # ✅ 確保載入 Base，這樣 Alembic 才知道有哪些表格

# Alembic 設定
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 讓 Alembic 知道我們的資料庫結構
target_metadata = Base.metadata  # ✅ 這行很重要！

def run_migrations_offline():
    """Offline 模式執行遷移"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Online 模式執行遷移"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()