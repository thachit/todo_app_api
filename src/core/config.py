import os

class Config:
    APP_NAME = os.getenv("APP_NAME", "Todo App")
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = os.getenv("APP_PORT", 8001)
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "nguyencothach1989@gmail.com")
    DATABASE_DRIVER = os.getenv("DATABASE_DRIVER", "postgresql+psycopg2")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", None)
    DATABASE_NAME = os.getenv("DATABASE_NAME", "postgres")
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", 1)
    SECRET_KEY = os.getenv("SECRET_KEY")
    TOKEN_EXPIRATION = os.getenv("TOKEN_EXPIRATION", 86400) # 1 day
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
    REFRESH_TOKEN_EXPIRATION = os.getenv("REFRESH_TOKEN_EXPIRATION", 2592000) # 30 days

