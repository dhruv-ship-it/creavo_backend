from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class SaleCreate(BaseModel):
    lead_id: UUID
    amount: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    payment_ref: Optional[str] = None


class SaleUpdate(BaseModel):
    status: Optional[str] = None
    payment_ref: Optional[str] = None
    access_granted: Optional[bool] = None


class SaleResponse(BaseModel):
    id: UUID
    lead_id: UUID
    amount: Optional[float]
    currency: Optional[str]
    status: Optional[str]
    payment_ref: Optional[str]
    access_granted: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
