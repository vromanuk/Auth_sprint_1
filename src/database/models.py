import uuid

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash

from src.database.db import Base, session_scope


class User(Base):
    __tablename__ = "users"

    # id = Column(
    #     UUID(as_uuid=True),
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     unique=True,
    #     nullable=False,
    # )
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    def __init__(self, login, password, is_admin=False):
        self.login = login
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User {self.login}>"

    @classmethod
    def find_by_username(cls, username: str):
        with session_scope() as session:
            return session.query(cls).filter_by(login=username).first()

    @classmethod
    def find_by_uuid(cls, id_: UUID):
        with session_scope() as session:
            return session.query(cls).filter_by(id=id_).first()
