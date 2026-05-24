from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class TopicCreate(BaseModel):
    title: str
    viral_score: Optional[int] = None
    status: Optional[str] = None


class TopicUpdate(BaseModel):
    title: Optional[str] = None
    viral_score: Optional[int] = None
    status: Optional[str] = None


class TopicResponse(BaseModel):
    id: UUID
    title: str
    viral_score: Optional[int]
    status: Optional[str]
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
