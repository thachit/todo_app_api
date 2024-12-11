from fastapi import HTTPException, status
from src.db.db import get_session
from src.models.task import Task

async def delete_task(task_id: str, user_id: str) -> None:
    with get_session() as session:
        task = session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

        if not task:
            raise HTTPException(detail="Task not found", status_code=status.HTTP_404_NOT_FOUND)

        session.delete(task)
        session.commit()

        return {"message": "Task deleted successfully"}