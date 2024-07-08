from sqlalchemy import Column, Integer, ForeignKey, Table
from app.config.data_source import Base

user_courses = Table(
    'user_courses', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)