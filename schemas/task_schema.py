def create_task_schema(task):
    return {
        "id": task.id,
        "title": task.title,
        "priority": task.priority,
        "energy_required": task.energy_required,
        "deadline": task.deadline.strftime("%Y-%m-%d %H:%M"),
        "estimated_duration": task.estimated_duration,
        "status": task.status
    }