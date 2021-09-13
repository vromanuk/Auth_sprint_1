import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from src.database.db import Base, session_scope


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    # id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    log_history = relationship("LogHistory")

    def __init__(self, login, password, is_admin=False):
        self.login = login
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User {self.login}>"

    @classmethod
    def find_by_login(cls, login: str):
        with session_scope() as session:
            return session.query(cls).filter_by(login=login).first()

    @classmethod
    def find_by_uuid(cls, id_: UUID):
        with session_scope() as session:
            return session.query(cls).filter_by(id=id_).first()


class LogHistory(Base):
    __tablename__ = "log_history"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    # id = Column(Integer, primary_key=True)
    logged_at = Column(DateTime, nullable=False, index=True)
    user_agent = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    # user_id = Column(Integer, ForeignKey('users.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
