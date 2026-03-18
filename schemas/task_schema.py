from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    priority: str
    energy_required: str
    deadline: datetime
    estimated_duration: int

    
