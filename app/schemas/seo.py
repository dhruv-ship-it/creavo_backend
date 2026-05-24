from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class SEOCreate(BaseModel):
    script_id: UUID
    description: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    hashtags: Optional[Dict[str, Any]] = None
    pinned_comment: Optional[str] = None


class SEOUpdate(BaseModel):
    description: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    hashtags: Optional[Dict[str, Any]] = None
    pinned_comment: Optional[str] = None


class SEOResponse(BaseModel):
    id: UUID
    script_id: UUID
    description: Optional[str]
    tags: Optional[Dict[str, Any]]
    hashtags: Optional[Dict[str, Any]]
    pinned_comment: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
