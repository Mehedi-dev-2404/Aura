import sqlite3
from models.task import Task

class TaskRepository:
    
    def __init__(self, db_path="aura.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_task(self, task):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (title, priority, energy_required, deadline, estimated_duration, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                task.title,
                task.priority,
                task.energy_required,
                task.deadline.strftime("%Y-%m-%d %H:%M"),
                task.estimated_duration,
                task.status
            ))
            task.id = cursor.lastrowid
    
    def get_all_tasks(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, priority, energy_required, deadline, estimated_duration, status FROM tasks")
            rows = cursor.fetchall()

        return [
            Task(
                id=row[0],
                title=row[1],
                priority=row[2],
                energy_required=row[3],
                deadline=row[4],
                estimated_duration=int(row[5]),
                status=row[6]
            )
            for row in rows
        ]
    
    def update_task(self, task):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks
                SET title = ?, priority = ?, energy_required = ?, deadline = ?, estimated_duration = ?, status = ?
                WHERE id = ?
            """, (
                task.title,
                task.priority,
                task.energy_required,
                task.deadline.strftime("%Y-%m-%d %H:%M"),
                task.estimated_duration,
                task.status,
                task.id
            ))


    def get_task_by_id(self, task_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, priority, energy_required, deadline, estimated_duration, status
                FROM tasks
                WHERE id = ?
            """, (task_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Task(
            id=row[0],
            title=row[1],
            priority=row[2],
            energy_required=row[3],
            deadline=row[4],
            estimated_duration=int(row[5]),
            status=row[6]
        )