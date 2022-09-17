from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class Vineyard(Base):
    __tablename__ = "vineyard"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    value = Column(Integer)
