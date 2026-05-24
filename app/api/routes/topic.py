from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicUpdate, TopicResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=List[TopicResponse])
@limiter.limit("100/minute")
def get_topics(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topics = db.query(Topic).filter(Topic.user_id == current_user.id).offset(skip).limit(limit).all()
    return topics


@router.get("/{topic_id}", response_model=TopicResponse)
@limiter.limit("100/minute")
def get_topic(
    request: Request,
    topic_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = db.query(Topic).filter(
        Topic.id == topic_id,
        Topic.user_id == current_user.id
    ).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    return topic


@router.post("/", response_model=TopicResponse)
@limiter.limit("100/minute")
def create_topic(
    request: Request,
    topic: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_topic = Topic(
        title=topic.title,
        viral_score=topic.viral_score,
        status=topic.status,
        user_id=current_user.id
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


@router.put("/{topic_id}", response_model=TopicResponse)
@limiter.limit("100/minute")
def update_topic(
    request: Request,
    topic_id: str,
    topic_update: TopicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = db.query(Topic).filter(
        Topic.id == topic_id,
        Topic.user_id == current_user.id
    ).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    update_data = topic_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(topic, field, value)
    
    db.commit()
    db.refresh(topic)
    return topic


@router.delete("/{topic_id}")
@limiter.limit("100/minute")
def delete_topic(
    request: Request,
    topic_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = db.query(Topic).filter(
        Topic.id == topic_id,
        Topic.user_id == current_user.id
    ).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    db.delete(topic)
    db.commit()
    return {"message": "Topic deleted successfully"}
