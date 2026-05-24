from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.script import Script
from app.models.topic import Topic
from app.schemas.script import ScriptCreate, ScriptUpdate, ScriptResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=List[ScriptResponse])
@limiter.limit("100/minute")
def get_scripts(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scripts = db.query(Script).filter(Script.user_id == current_user.id).offset(skip).limit(limit).all()
    return scripts


@router.get("/{script_id}", response_model=ScriptResponse)
@limiter.limit("100/minute")
def get_script(
    request: Request,
    script_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    script = db.query(Script).filter(
        Script.id == script_id,
        Script.user_id == current_user.id
    ).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )
    return script


@router.post("/", response_model=ScriptResponse)
@limiter.limit("100/minute")
def create_script(
    request: Request,
    script: ScriptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate topic exists and belongs to user
    topic = db.query(Topic).filter(
        Topic.id == script.topic_id,
        Topic.user_id == current_user.id
    ).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found or doesn't belong to you"
        )
    
    db_script = Script(
        content=script.content,
        script_type=script.script_type,
        version=script.version,
        topic_id=script.topic_id,
        user_id=current_user.id
    )
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script


@router.put("/{script_id}", response_model=ScriptResponse)
@limiter.limit("100/minute")
def update_script(
    request: Request,
    script_id: str,
    script_update: ScriptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    script = db.query(Script).filter(
        Script.id == script_id,
        Script.user_id == current_user.id
    ).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )
    
    update_data = script_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(script, field, value)
    
    db.commit()
    db.refresh(script)
    return script
