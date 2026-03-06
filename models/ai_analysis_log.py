from decimal import Decimal
from datetime import datetime
from typing import Optional
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AiAnalysisLog(db.Model):
    """ORM model representing a single AI image analysis log entry."""

    __tablename__ = "ai_analysis_log"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_path: Optional[str] = db.Column(db.String(255), nullable=True)
    is_success: bool = db.Column("success", db.Boolean, nullable=False)
    message: Optional[str] = db.Column(db.String(255), nullable=True)
    class_label: Optional[int] = db.Column("class", db.Integer, nullable=True)
    confidence: Optional[Decimal] = db.Column(db.Numeric(5, 4), nullable=True)
    request_timestamp: Optional[datetime] = db.Column(db.DateTime, nullable=True)
    response_timestamp: Optional[datetime] = db.Column(db.DateTime, nullable=True)

    def to_dict(self) -> dict:
        """Return a dictionary representation of this log entry."""
        return {
            "id": self.id,
            "image_path": self.image_path,
            "is_success": self.is_success,
            "message": self.message,
            "class_label": self.class_label,
            "confidence": float(self.confidence) if self.confidence is not None else None,
            "request_timestamp": self.request_timestamp.isoformat() if self.request_timestamp else None,
            "response_timestamp": self.response_timestamp.isoformat() if self.response_timestamp else None,
        }
