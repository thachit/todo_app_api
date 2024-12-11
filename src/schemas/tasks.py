import datetime
from pydantic import BaseModel, field_validator, EmailStr, Field
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