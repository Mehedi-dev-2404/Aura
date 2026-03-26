from fastapi import FastAPI
from typing import List
from repositories.task_repository import TaskRepository
from schemas.task_schema import TaskCreate, TaskResponse
from models.task import Task
from fastapi import HTTPException

app = FastAPI()
repo = TaskRepository()

@app.get("/")
def root():
    return {"message": "Aura API running"}

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    return repo.get_all_tasks()

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = repo.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=TaskResponse)
def create_task(task_data: TaskCreate):
    task = Task(
        title=task_data.title,
        priority=task_data.priority,
        energy_required=task_data.energy_required,
        deadline=task_data.deadline,
        estimated_duration=task_data.estimated_duration,
        status="PENDING"
    )

    repo.create_task(task)
    return task