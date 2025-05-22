from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL  # Это будет твой URL для подключения к базе данных

# Создание базы
Base = declarative_base()

# Подключение к базе данных (например, SQLite, PostgreSQL или другой)
# DATABASE_URL должен быть определен в config.py или непосредственно в этом файле
DATABASE_URL = "sqlite:///./test.db"  # Это пример для SQLite. Для PostgreSQL или другого изменишь строку подключения.

# Настройка движка для SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Это для SQLite, в других БД `connect_args` не нужно

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения текущей сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
