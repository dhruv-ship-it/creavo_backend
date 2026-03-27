import uuid
from sqlalchemy import String, Integer, DateTime, Text, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Script(Base):
    __tablename__ = "scripts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    script_type = Column(String(50))  # LONG or SHORT
    version = Column(Integer)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    topic = relationship("Topic", back_populates="scripts")
    user = relationship("User", back_populates="scripts")
    seo = relationship("SEO", back_populates="script", uselist=False)
