from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.script import Script
from app.models.seo import SEO
from app.schemas.seo import SEOCreate, SEOUpdate, SEOResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{script_id}", response_model=SEOResponse)
@limiter.limit("100/minute")
def get_seo(
    request: Request,
    script_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify script belongs to user
    script = db.query(Script).filter(
        Script.id == script_id,
        Script.user_id == current_user.id
    ).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )
    
    seo = db.query(SEO).filter(SEO.script_id == script_id).first()
    if not seo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SEO data not found"
        )
    return seo


@router.post("/", response_model=SEOResponse)
@limiter.limit("100/minute")
def create_or_update_seo(
    request: Request,
    seo_data: SEOCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify script belongs to user
    script = db.query(Script).filter(
        Script.id == seo_data.script_id,
        Script.user_id == current_user.id
    ).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )
    
    # Check if SEO already exists (one-to-one)
    existing_seo = db.query(SEO).filter(SEO.script_id == seo_data.script_id).first()
    
    if existing_seo:
        # Update existing SEO
        update_data = seo_data.model_dump(exclude_unset=True, exclude={"script_id"})
        for field, value in update_data.items():
            setattr(existing_seo, field, value)
        db.commit()
        db.refresh(existing_seo)
        return existing_seo
    else:
        # Create new SEO
        db_seo = SEO(
            script_id=seo_data.script_id,
            description=seo_data.description,
            tags=seo_data.tags,
            hashtags=seo_data.hashtags,
            pinned_comment=seo_data.pinned_comment
        )
        db.add(db_seo)
        db.commit()
        db.refresh(db_seo)
        return db_seo


@router.put("/{script_id}", response_model=SEOResponse)
@limiter.limit("100/minute")
def update_seo(
    request: Request,
    script_id: str,
    seo_update: SEOUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify script belongs to user
    script = db.query(Script).filter(
        Script.id == script_id,
        Script.user_id == current_user.id
    ).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )
    
    seo = db.query(SEO).filter(SEO.script_id == script_id).first()
    if not seo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SEO data not found"
        )
    
    update_data = seo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(seo, field, value)
    
    db.commit()
    db.refresh(seo)
    return seo
