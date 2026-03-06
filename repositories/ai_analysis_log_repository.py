"""Repository for AiAnalysisLog database operations."""

from models.ai_analysis_log import db, AiAnalysisLog


class AiAnalysisLogRepository:
    """Handles all database operations for AiAnalysisLog."""

    def save(self, log: AiAnalysisLog) -> None:
        """Persist a new log entry to the database.

        Args:
            log: The AiAnalysisLog instance to save.
        """
        db.session.add(log)
        db.session.commit()

    def find_latest(self, limit: int = 50) -> list[AiAnalysisLog]:
        """Return the most recent log entries, ordered by id descending.

        Args:
            limit: Maximum number of records to return.

        Returns:
            A list of AiAnalysisLog instances.
        """
        return AiAnalysisLog.query.order_by(AiAnalysisLog.id.desc()).limit(limit).all()
