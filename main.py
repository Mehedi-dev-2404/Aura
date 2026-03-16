from fastapi import FastAPI
from repositories.task_repository import TaskRepository


app = FastAPI()
repo = TaskRepository()

@app.get("/")
def root():
    return {"message": "Aura API running"}
@app.get("/tasks")
def get_tasks():
    return repo.get_all_tasks()