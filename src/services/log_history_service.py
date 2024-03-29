from uuid import UUID

from src.database.db import session_scope
from src.database.models import LogHistory
from src.schemas.log_history import LogHistorySchema


class LogHistoryService:
    @classmethod
    def create_entry(cls, entry: dict):
        with session_scope() as session:
            log_history = LogHistorySchema().load(entry, session=session)
            session.add(log_history)
            session.commit()

    @classmethod
    def list_histories(cls, user_id: UUID):
        schema = LogHistorySchema(many=True)
        with session_scope() as session:
            log_histories_raw = (
                session.query(LogHistory).filter_by(user_id=user_id).all()
            )
            return schema.dump(log_histories_raw)
