import sqlite3
from models.task import Task

class TaskRepository:
    
    
    def _get_connection(self):
        conn = sqlite3.connect("aura.db")
        return conn