from sqlalchemy import Column, Integer, String, func, desc
from database import Base, SessionLocal
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)

    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)


