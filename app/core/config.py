import os

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prototype.db")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_prototype_key_123")
    ALGORITHM = "HS256"

config = Config()
