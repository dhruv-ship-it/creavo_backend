from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ScriptCreate(BaseModel):
    content: str
    script_type: Optional[str] = None
    version: Optional[int] = None
    topic_id: UUID


class ScriptUpdate(BaseModel):
    content: Optional[str] = None
    script_type: Optional[str] = None
    version: Optional[int] = None


class ScriptResponse(BaseModel):
    id: UUID
    content: str
    script_type: Optional[str]
    version: Optional[int]
    topic_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
