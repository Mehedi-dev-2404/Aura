from repositories.task_repository import TaskRepository
from models.task import Task
from datetime import datetime

repo = TaskRepository()

print("---- CREATE ----")
task = Task(
    title="Delete Test",
    priority="HIGH",
    energy_required="MEDIUM",
    deadline=datetime(2024, 12, 31, 12, 0),
    estimated_duration=60
)

repo.create_task(task)
print("Created Task ID:", task.id)


print("\n---- READ ALL ----")
tasks = repo.get_all_tasks()
for t in tasks:
    print(t.id, t.title, t.status)


print("\n---- READ BY ID ----")
single = repo.get_task_by_id(task.id)
print(single.id, single.title)


print("\n---- UPDATE ----")
single.status = "COMPLETED"
repo.update_task(single)

updated = repo.get_task_by_id(task.id)
print("Updated status:", updated.status)


print("\n---- DELETE ----")
repo.delete_task(task.id)

deleted = repo.get_task_by_id(task.id)
print("After delete:", deleted)