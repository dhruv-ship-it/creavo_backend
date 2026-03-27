import uuid
from sqlalchemy import String, DateTime, Text, Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class SEO(Base):
    __tablename__ = "seo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text)
    tags = Column(JSON)
    hashtags = Column(JSON)
    pinned_comment = Column(Text)
    script_id = Column(UUID(as_uuid=True), ForeignKey("scripts.id"), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    script = relationship("Script", back_populates="seo")

    __table_args__ = (
        UniqueConstraint('script_id', name='uq_seo_script_id'),
    )
