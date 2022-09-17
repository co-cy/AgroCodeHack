from sqlalchemy import Column, String, Integer
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    token = Column(String(512), unique=True, index=True)
    login = Column(String(128), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
