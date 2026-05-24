from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class CommentCreate(BaseModel):
    video_id: Optional[str] = None
    body: str
    author_name: str


class CommentUpdate(BaseModel):
    reply_text: Optional[str] = None


class CommentResponse(BaseModel):
    id: UUID
    video_id: Optional[str]
    body: str
    author_name: str
    replied: bool
    reply_text: Optional[str]
    replied_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
