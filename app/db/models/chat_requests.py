from datetime import datetime

from app.core.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Enum as SqlEnum, DateTime
from sqlalchemy.orm import relationship 
from enum import Enum

class ChatRequestStatus(str, Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

class ChatRequest(Base):
    __tablename__ = "chat_requests"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SqlEnum(ChatRequestStatus), default=ChatRequestStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
