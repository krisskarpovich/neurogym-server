from __future__ import with_statement
import sys
from os.path import abspath, dirname
sys.path.insert(0, abspath(dirname(__file__)))

from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from logging.config import fileConfig

from alembic import context

# Импортируем метаданные
from database import Base  # Здесь должен быть импорт твоей базы

# Настроим target_metadata
target_metadata = Base.metadata  # Это объект MetaData, который Alembic будет использовать для создания миграций

# Обработчик конфигурации
config = context.config

fileConfig(config.config_file_name)

# Получаем URL подключения из конфигурации
config.set_main_option('sqlalchemy.url', 'sqlite:///./test.db')  # Укажи свой правильный URL подключения

# Настройка подключения к базе данных
engine = create_engine(config.get_main_option("sqlalchemy.url"))

# Обновление миграции
def run_migrations_online():
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if __name__ == "__main__":
    run_migrations_online()
