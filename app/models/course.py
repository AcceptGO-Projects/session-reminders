from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.config.data_source import Base
from app.models.user_course import user_courses

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    users = relationship("User", secondary=user_courses, back_populates="courses")
    reminders = relationship("Reminder", back_populates="course")
    
