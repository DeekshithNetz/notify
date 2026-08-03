from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    google_id = Column(String(100), unique=True, nullable=False)

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    role = Column(String(20), default="user", nullable=False)

    fcm_token = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)