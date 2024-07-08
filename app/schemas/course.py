from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from typing_extensions import Annotated

class CourseBase(BaseModel):
    name: Annotated[str, Field(max_length=100, example="Math 101")]
    description: Optional[Annotated[str, Field(max_length=255, example="Introductory Math Course")]] = None
    
    model_config = ConfigDict(from_attributes=True)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class Course(CourseBase):
    id: Annotated[int, Field(ge=1, example=1)]
    
class CourseDetails(Course):
    reminders: List[int] = []
    users: List[int] = []

