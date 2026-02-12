from database import get_connection
from models.task import Task

class TaskRepository:

    def add_task(self, task: Task):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, deadline, estimated_duration, priority, energy_required, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            task.title,
            task.deadline.strftime("%Y-%m-%d %H:%M"),
            task.estimated_duration,
            task.priority,
            task.energy_required,
            task.status
        ))

        conn.commit()
        conn.close()