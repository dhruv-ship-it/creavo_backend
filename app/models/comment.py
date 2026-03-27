import uuid
from sqlalchemy import String, DateTime, Text, Column, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(String(255))
    body = Column(Text, nullable=False)
    author_name = Column(String(255), nullable=False)
    replied = Column(Boolean, default=False)
    reply_text = Column(Text)
    replied_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
