"""
Email Model
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class EmailType(str, Enum):
    INITIAL = "initial"
    FOLLOW_UP_1 = "follow_up_1"
    FOLLOW_UP_2 = "follow_up_2"
    FOLLOW_UP_3 = "follow_up_3"
    REPLY = "reply"
    CUSTOM = "custom"


class EmailStatus(str, Enum):
    DRAFT = "draft"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    REPLIED = "replied"
    BOUNCED = "bounced"
    FAILED = "failed"


class Email(Base):
    """Email model"""
    
    __tablename__ = "emails"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Lead relationship
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Email Details
    email_type: Mapped[str] = mapped_column(String(20), default=EmailType.INITIAL)
    
    to_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    from_email: Mapped[str] = mapped_column(String(255), nullable=False)
    from_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    body_html: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default=EmailStatus.DRAFT, index=True)
    
    # Tracking
    is_opened: Mapped[bool] = mapped_column(Boolean, default=False)
    is_clicked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_replied: Mapped[bool] = mapped_column(Boolean, default=False)
    
    opened_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    clicked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    replied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    open_count: Mapped[int] = mapped_column(Integer, default=0)
    click_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # External IDs
    message_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    thread_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    
    # Error handling
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Metadata
    personalization_data: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)
    
    # Scheduling
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    lead: Mapped["Lead"] = relationship("Lead", back_populates="emails")
    
    def __repr__(self) -> str:
        return f"<Email(id={self.id}, to='{self.to_email}')>"