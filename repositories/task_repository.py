import sqlite3
from models.task import Task

class TaskRepository:
    
    def __init__(self, db_path="aura.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_task(self, task):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, priority, energy_required, deadline, estimated_duration, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (task.title, task.priority, task.energy_required, task.deadline.strftime("%Y-%m-%d %H:%M"), task.estimated_duration, task.status))
        conn.commit()
        conn.close()
    
    def get_all_tasks(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, priority, energy_required, deadline, estimated_duration, status FROM tasks")
        rows = cursor.fetchall()
        conn.close()
        return [Task(id=row[0], title=row[1], priority=row[2], energy_required=row[3], deadline=row[4], estimated_duration=row[5], status=row[6]) for row in rows]
    
    def update_task(self, task):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET title = ?, priority = ?, energy_required = ?, deadline = ?, estimated_duration = ?, status = ?
            WHERE id = ?
        """, (task.title, task.priority, task.energy_required, task.deadline.strftime("%Y-%m-%d %H:%M"), task.estimated_duration, task.status, task.id))
        conn.commit()
        conn.close()