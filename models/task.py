from datetime import datetime

class Task:


    def __init__(self, 
                 title, 
                 priority, 
                 energy_required, 
                 deadline, 
                 estimated_duration, 
                 status = 'PENDING',
                 id = None):
        
        self.id = id
        self.title = title
        self.priority = priority
        self.energy_required = energy_required
        self.deadline = deadline
        self.estimated_duration = estimated_duration
        self.status = status
        if isinstance(deadline, str):
            self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        else:
            self.deadline = deadline
        self.validate()

    def validate(self):
        if not self.title:
            raise ValueError("Title cannot be empty")
        if self.priority not in ['LOW', 'MEDIUM', 'HIGH']:
            raise ValueError("Priority must be 'LOW', 'MEDIUM', or 'HIGH'")
        if self.status not in ['PENDING', 'COMPLETED', 'SKIPPED']:
            raise ValueError("Status must be 'PENDING', 'COMPLETED', or 'SKIPPED'")
        if self.energy_required not in ['LOW', 'MEDIUM', 'HIGH']:
            raise ValueError("Energy required must be LOW, MEDIUM, or HIGH")
        if self.estimated_duration <= 0:
            raise ValueError("Estimated duration must be greater than 0")
        
