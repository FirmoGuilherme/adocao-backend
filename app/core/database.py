from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import config

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        self.engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

db_manager = DatabaseManager()

Base = declarative_base()

def get_db():
    db = db_manager.SessionLocal()
    try:
        yield db
    finally:
        db.close()
