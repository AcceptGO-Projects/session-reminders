from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.data_source import Base

class UserReminder(Base):
    __tablename__ = "user_reminders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reminder_id = Column(Integer, ForeignKey("reminders.id"), nullable=False)
    status = Column(String(20), default='pending', nullable=False)

    user = relationship("User", back_populates="user_reminders")
    reminder = relationship("Reminder", back_populates="user_reminders")