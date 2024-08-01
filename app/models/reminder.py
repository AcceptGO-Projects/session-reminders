from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import pytz

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

    def save(self, session):
        if self.due_date.tzinfo is None:
            self.due_date = self.due_date.replace(tzinfo=pytz.utc)
        else:
            self.due_date = self.due_date.astimezone(pytz.utc)
        session.add(self)
        session.commit()
        session.refresh(self)
