from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RpaTask(Base):
    __tablename__ = "rpa_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_no = Column(String(50), unique=True, nullable=False)
    task_type = Column(String(20), nullable=False)
    business_key = Column(String(50), nullable=False)
    params = Column(Text)
    status = Column(String(20), default="PENDING")
    retry_count = Column(Integer, default=0)
    max_retry = Column(Integer, default=3)
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())