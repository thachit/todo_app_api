from fastapi import HTTPException, status
from src.schemas.tasks import UpdateTaskDto, TaskResponse
from src.db.db import get_session
from src.models.task import Task

async def update_task(task_id: str, user_id: str, params: UpdateTaskDto) -> TaskResponse:
    with get_session() as session:
        task = session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

        if not task:
            raise HTTPException(detail="Task not found", status_code=status.HTTP_404_NOT_FOUND)

        update_fields = list(params.model_fields.keys())
        for field in update_fields:
            if getattr(params, field) is not None:
                if field == 'priority':
                    setattr(task, field, params.priority.value)
                else:
                    setattr(task, field, getattr(params, field))
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(detail=f"{str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        updated_task = session.query(Task).filter(Task.id == task_id).first()
        return updated_task.to_dict()
