
SECRET_KEY = "refresh_token" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 день, можно изменить
DATABASE_URL = "sqlite:///./test.db"  # Файл базы данных будет в корне проекта

# DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/neurogym_db"
