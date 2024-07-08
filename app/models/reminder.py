# app/models/reminder.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.config.data_source import Base
from app.schemas.reminder import ReminderCategory

class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(Enum(ReminderCategory), nullable=False)
    due_date = Column(DateTime, nullable=False)
    course = relationship("Course", back_populates="reminders")
    user_reminders = relationship("UserReminder", back_populates="reminder")
