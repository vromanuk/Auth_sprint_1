from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LogHistorySchema(BaseModel):
    id: UUID
    logged_at: datetime
    user_agent: str
    ip: str
    refresh_token: str
    expires_at: datetime
    user_id: UUID

    class Config:
        orm_mode = True
