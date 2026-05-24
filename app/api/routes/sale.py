from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.sale import Sale
from app.models.lead import Lead
from app.schemas.sale import SaleCreate, SaleUpdate, SaleResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=List[SaleResponse])
@limiter.limit("100/minute")
def get_sales(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sales = db.query(Sale).offset(skip).limit(limit).all()
    return sales


@router.get("/{sale_id}", response_model=SaleResponse)
@limiter.limit("100/minute")
def get_sale(
    request: Request,
    sale_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale


@router.post("/", response_model=SaleResponse)
@limiter.limit("100/minute")
def create_sale(
    request: Request,
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate lead exists
    lead = db.query(Lead).filter(Lead.id == sale.lead_id).first()
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    db_sale = Sale(
        lead_id=sale.lead_id,
        amount=sale.amount,
        currency=sale.currency,
        status=sale.status,
        payment_ref=sale.payment_ref
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.put("/{sale_id}", response_model=SaleResponse)
@limiter.limit("100/minute")
def update_sale(
    request: Request,
    sale_id: str,
    sale_update: SaleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    update_data = sale_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sale, field, value)
    
    db.commit()
    db.refresh(sale)
    return sale
