import datetime
from sqlalchemy.orm import validates
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from src.db.db import Base

PRIORITY_MAP = {
    "low": 0,
    "medium": 1,
    "high": 2
}

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, default=datetime.datetime.utcnow)
    priority = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    @validates('priority')
    def validate_priority(self, key, value):
        return PRIORITY_MAP.get(value, 1)

    @property
    def priority_label(self):
        for key, val in PRIORITY_MAP.items():
            if val == self.priority:
                return key
        return "medium"

    def to_dict(self):
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "priority": self.priority_label,
                "status": self.status,
                "due_date": self.due_date.isoformat(),
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
            }
