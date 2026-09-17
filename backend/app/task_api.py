from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import json
import uuid

from .db import init_db, get_db
from .models.task import RpaTask

app = FastAPI(title="RPA任务队列")


@app.on_event("startup")
def startup():
    init_db()


class TaskCreate(BaseModel):
    task_type: str
    business_key: str
    params: Optional[dict] = None


@app.post("/api/tasks")
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    existing = db.query(RpaTask).filter(
        RpaTask.business_key == data.business_key,
        RpaTask.task_type == data.task_type,
        RpaTask.status.in_(["PENDING", "RUNNING"])
    ).first()
    if existing:
        return {"code": 200, "message": "任务已存在", "data": existing}

    task_no = f"TASK{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4]}"
    task = RpaTask(
        task_no=task_no,
        task_type=data.task_type,
        business_key=data.business_key,
        params=json.dumps(data.params or {}, ensure_ascii=False),
        status="PENDING"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"code": 200, "message": "创建成功", "data": task}


@app.get("/api/tasks")
def list_tasks(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(RpaTask)
    if status:
        query = query.filter(RpaTask.status == status)
    tasks = query.order_by(RpaTask.id.desc()).all()
    return {"code": 200, "message": "查询成功", "data": tasks}


@app.get("/api/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(RpaTask).filter(RpaTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"code": 200, "message": "查询成功", "data": task}


@app.post("/api/tasks/{task_id}/retry")
def retry_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(RpaTask).filter(RpaTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    task.status = "PENDING"
    task.retry_count = 0
    task.error_message = None
    db.commit()
    db.refresh(task)
    return {"code": 200, "message": "任务已重置", "data": task}