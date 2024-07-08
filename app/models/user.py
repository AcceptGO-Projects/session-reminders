from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.data_source import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    courses = relationship("Course", secondary="user_courses", back_populates="users")
    user_reminders = relationship("UserReminder", back_populates="user")
