from fastapi import FastAPI
from typing import List
from repositories.task_repository import TaskRepository
from schemas.task_schema import TaskResponse

app = FastAPI()
repo = TaskRepository()

@app.get("/")
def root():
    return {"message": "Aura API running"}

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    return repo.get_all_tasks()