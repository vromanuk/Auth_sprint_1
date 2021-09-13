import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash

from src.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.login}>"
