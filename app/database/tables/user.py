from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    token = Column(String(512), unique=True, index=True)
    login = Column(String(128), unique=True, index=True, nullable=False)

    vineyards = relationship("Vineyard", uselist=True)

    password = Column(String(128), nullable=False)
