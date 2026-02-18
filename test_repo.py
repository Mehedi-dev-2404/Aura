from repositories.task_repository import TaskRepository
from models.task import Task
from datetime import datetime

repo = TaskRepository()

task = Task(
    title="Deep Work",
    priority="HIGH",
    energy_required="HIGH",
    deadline=datetime(2026, 2, 10, 18, 0),
    estimated_duration=90
)
repo.create_task(task)
