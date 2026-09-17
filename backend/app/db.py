from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.task import Base

DB_USER = "root"
DB_PASSWORD = "123456"          # phpStudy 默认密码通常是 root
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "feishu_rpa"

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()