from fastapi import FastAPI
from repositories.task_repository import TaskRepository


app = FastAPI()
repo = TaskRepository()

@app.get("/")
def root():
    return repo.get_all_tasks()