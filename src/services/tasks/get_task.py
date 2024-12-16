from sqlalchemy.sql import operators
from sqlalchemy import asc, desc, func
from src.schemas.tasks import TaskListResponse, GetTaskQueryDto
from src.db.db import get_session
from src.models.task import Task

def build_filter_query(column, value, operator: str) -> str:
    operator_mapping = {
        "gte": operators.ge,
        "gt": operators.gt,
        "lte": operators.le,
        "lt": operators.lt,
        "eq": operators.eq,
        "neq": operators.ne
    }

    sql_operator = operator_mapping.get(operator, operators.ge)
    return sql_operator(column, value)

def build_order_query(order: str, order_by: str):
    if order == "asc":
        return asc(order_by)
    return desc(order_by)


async def get_tasks(user_id: str, query: GetTaskQueryDto) -> TaskListResponse:
    with (get_session() as session):
        tasks = session.query(Task).filter(Task.user_id == user_id)

        if query.due_date and query.due_date_operator:
            due_date_query = build_filter_query(Task.due_date, query.due_date, query.due_date_operator)
            tasks = tasks.filter(due_date_query)
        if query.status:
            tasks = tasks.filter(Task.status == query.status)

        if query.order and query.order_by:
            order_by_query = build_order_query(query.order, query.order_by)
            tasks = tasks.order_by(order_by_query)

        total_tasks = tasks.count()
        tasks = tasks.limit(query.limit).offset((query.page - 1) * query.limit).all()
        return {
            "page": query.page,
            "limit": query.limit,
            "total_tasks": total_tasks,
            "tasks": [task.to_dict() for task in tasks]
        }
