from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import enum
from typing_extensions import Annotated

class ReminderCategory(str, enum.Enum):
    ALERT = "alert"
    RESOURCE = "resource"

class ReminderBase(BaseModel):
    course_id: Annotated[int, Field(ge=1, example=1)]
    message: Annotated[str, Field(max_length=1500, example="This is a reminder message.")]
    category: ReminderCategory
    due_date: Annotated[datetime, Field(example="2023-12-31T23:59:59")]
    
    model_config = ConfigDict(from_attributes=True)

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: Annotated[int, Field(ge=1, example=1)]
