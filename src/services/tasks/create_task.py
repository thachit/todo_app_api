from fastapi import HTTPException
from src.schemas.tasks import CreateTaskDto, TaskResponse
from src.db.db import get_session
from src.models.task import Task

async def create_task(user_id: str, params: CreateTaskDto) -> TaskResponse:
    try:
        with get_session() as session:
            new_task = Task(
                title=params.title,
                description=params.description,
                due_date=params.due_date,
                priority=params.priority.value,
                status=params.status,
                user_id=user_id
            )
            session.add(new_task)
            session.commit()

            return new_task.to_dict()
    except Exception as e:
        session.rollback()
        raise HTTPException(detail=f"Internal Server Error", status_code=500)




