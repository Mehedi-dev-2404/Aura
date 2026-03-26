from fastapi import FastAPI
from typing import List
from repositories.task_repository import TaskRepository
from schemas.task_schema import TaskCreate, TaskResponse

app = FastAPI()
repo = TaskRepository()

@app.get("/")
def root():
    return {"message": "Aura API running"}

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    return repo.get_all_tasks()

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    new_task = repo.create_task(task)
    return new_task