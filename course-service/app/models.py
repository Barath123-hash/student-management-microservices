from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    duration = Column(String(50), nullable=False)
    instructor = Column(String(100), nullable=False)
