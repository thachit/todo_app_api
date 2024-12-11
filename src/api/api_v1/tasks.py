from fastapi import Depends
from fastapi import APIRouter
from src.services.tasks.create_task import create_task
from src.services.tasks.update_task import update_task
from src.services.tasks.delete_task import delete_task
from src.schemas.tasks import CreateTaskDto, UpdateTaskDto, TaskResponse
from src.utils.jwt_token import required_token
task_router_v1 = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@task_router_v1.post("")
async def create_task_api(
        params: CreateTaskDto,
        user_id = Depends(required_token)
) -> TaskResponse:
    response = await create_task(user_id, params)
    return response

@task_router_v1.patch("/{task_id}")
async def update_task_api(
        task_id: str,
        params: UpdateTaskDto,
        user_id = Depends(required_token)
):
    responses = await update_task(task_id, user_id, params)
    return responses

@task_router_v1.delete("/{task_id}")
async def delete_task_api(
        task_id: str,
        user_id = Depends(required_token)
):
    responses = await delete_task(task_id, user_id)
    return responses