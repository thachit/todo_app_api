import datetime
from fastapi import HTTPException
from src.models.task import Task
from fastapi import Query, status as http_status

from pydantic import BaseModel, field_validator, Field
from typing import Optional
from enum import Enum

class TaskPriority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class TaskStatus(str, Enum):
    new = 'new'
    in_progress = 'in_progress'
    pending = 'pending'
    done = 'done'


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[str]
    priority: Optional[str]
    status: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TaskListResponse(BaseModel):
    page: int
    limit: int
    total_tasks: int
    tasks: list[TaskResponse]


class TaskBaseDto(BaseModel):
    due_date: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    @field_validator('due_date')
    def validate_due_date(due_date: str):
        if not due_date:
            return None
        if due_date.endswith('Z'):
            due_date = due_date.replace('Z', '+00:00')

        due_date_utc = datetime.datetime.fromisoformat(due_date).astimezone(datetime.timezone.utc)
        current_utc = datetime.datetime.now(datetime.timezone.utc)
        if due_date_utc < current_utc:
            raise ValueError("Due date must be in the future")

        return due_date_utc


class CreateTaskDto(TaskBaseDto):
    title: str
    priority: Optional[TaskPriority] = Field(default=TaskPriority.medium)
    status: Optional[TaskStatus] = Field(default=TaskStatus.new)


class UpdateTaskDto(TaskBaseDto):
    title: Optional[str] = Field(default=None)
    priority: Optional[TaskPriority] = Field(default=None)
    status: Optional[TaskStatus] = Field(default=None)


class GetTaskQueryOrder(str, Enum):
    asc = 'asc'
    desc = 'desc'


class GetTaskQueryDueDateOperator(str, Enum):
    gte = 'gte'
    gt = 'gt'
    lte = 'lte'
    lt = 'lt'
    eq = 'eq'
    neq = 'neq'


class GetTaskQueryDto(BaseModel):
    page: Optional[int] = Field(default=1)
    limit: Optional[int] = Field(default=0)
    order: Optional[GetTaskQueryOrder] = Field(default=GetTaskQueryOrder.asc)
    order_by: Optional[str] = Field(default="priority")
    title: Optional[str] = Field(default=None)
    due_date: Optional[str] = Field(default=None)
    due_date_operator: Optional[GetTaskQueryDueDateOperator] = Field(default=GetTaskQueryDueDateOperator.gte)
    status: Optional[TaskStatus] = Field(default=None)

    @classmethod
    async def as_model(
            cls,
            page: int = Query(default=1),
            limit: int = Query(default=10),
            order: GetTaskQueryOrder = Query(default=GetTaskQueryOrder.asc),
            order_by: str = Query(default="priority"),
            title: str = Query(default=None),
            due_date: str = Query(default=None),
            due_date_operator: GetTaskQueryDueDateOperator = Query(default=None),
            status: TaskStatus = Query(default=None)
    ):
        query = GetTaskQueryDto(
            page=page,
            limit=limit,
            order=order,
            order_by=order_by,
            title=title,
            due_date=due_date,
            due_date_operator=due_date_operator,
            status=status
        )
        return query

    @field_validator('due_date')
    def validate_due_date(due_date: str):
        if not due_date:
            return None
        if due_date.endswith('Z'):
            due_date = due_date.replace('Z', '+00:00')

        due_date_utc = datetime.datetime.fromisoformat(due_date).astimezone(datetime.timezone.utc)

        return due_date_utc

    @field_validator('order_by')
    def validate_order_by(order_by: str):
        column = getattr(Task, order_by, None)
        if not column:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid order by field: {order_by}"
            )
        return order_by