from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    priority: str
    energy_required: str
    deadline: datetime
    estimated_duration: int


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    energy_required: str
    deadline: datetime
    estimated_duration: int
    status: str

    class Config:
        from_attributes = True