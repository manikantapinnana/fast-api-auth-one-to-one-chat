from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class ChatRequestStatus(str, Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class ChatRequestCreate(BaseModel):
    sender_id: int
    receiver_id: int


class ChatRequestResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: ChatRequestStatus
    created_at: datetime

    model_config = {"from_attributes": True}
