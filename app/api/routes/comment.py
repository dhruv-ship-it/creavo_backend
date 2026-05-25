from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_db, require_roles
from app.models.user import User
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{video_id}", response_model=List[CommentResponse])
@limiter.limit("100/minute")
def get_comments_by_video(
    request: Request,
    video_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Public endpoint - anyone can view comments for a video."""
    comments = db.query(Comment).filter(
        Comment.video_id == video_id
    ).offset(skip).limit(limit).all()
    return comments


@router.post("/", response_model=CommentResponse)
@limiter.limit("100/minute")
def create_comment(
    request: Request,
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    """Public endpoint - anyone can create a comment."""
    db_comment = Comment(
        video_id=comment.video_id,
        body=comment.body,
        author_name=comment.author_name,
        replied=False
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.post("/reply/{comment_id}", response_model=CommentResponse)
@limiter.limit("100/minute")
def reply_to_comment(
    request: Request,
    comment_id: str,
    reply_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "CONTENT"]))
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if not reply_data.reply_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reply text is required"
        )
    
    comment.replied = True
    comment.reply_text = reply_data.reply_text
    comment.replied_at = datetime.utcnow()
    
    db.commit()
    db.refresh(comment)
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
@limiter.limit("100/minute")
def update_comment(
    request: Request,
    comment_id: str,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "CONTENT"]))
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    update_data = comment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
    
    db.commit()
    db.refresh(comment)
    return comment
