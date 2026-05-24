from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class LeadCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    tag: Optional[str] = None
    status: Optional[str] = None
    lead_metadata: Optional[Dict[str, Any]] = None


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    tag: Optional[str] = None


class LeadResponse(BaseModel):
    id: UUID
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    tag: Optional[str]
    status: Optional[str]
    lead_metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
