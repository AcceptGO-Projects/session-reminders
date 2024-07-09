from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config.data_source import Base

class UserCourse(Base):
    __tablename__ = 'user_courses'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)