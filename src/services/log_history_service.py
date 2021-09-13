from datetime import datetime
from uuid import UUID

from src.database.db import session_scope
from src.database.models import LogHistory
from src.schemas.log_history import LogHistorySchema


class LogHistoryService:
    @classmethod
    def create_entry(cls, logged_at: datetime, user_agent: str, ip: str, user_id: UUID):
        with session_scope() as session:
            log_history = LogHistory(
                logged_at=logged_at, user_agent=user_agent, ip=ip, user_id=user_id
            )
            session.add(log_history)
            session.commit()

    @classmethod
    def list_histories(cls, user_id: UUID):
        with session_scope() as session:
            log_histories_raw = (
                session.query(LogHistory).filter_by(user_id=user_id).all()
            )
            return [
                LogHistorySchema.from_orm(log_history).dict()
                for log_history in log_histories_raw
            ]
