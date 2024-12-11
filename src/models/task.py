import datetime
import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from src.db.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, default=datetime.datetime.utcnow)
    priority = Column(String, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "priority": self.priority,
                "status": self.status,
                "due_date": self.due_date.isoformat(),
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
            }
