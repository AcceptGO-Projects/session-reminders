from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Optional
from typing_extensions import Annotated

class UserBase(BaseModel):
    code: Annotated[str, Field(max_length=50, example="U12345")]
    first_name: Annotated[str, Field(max_length=100, example="John")]
    last_name: Annotated[str, Field(max_length=100, example="Doe")]
    email: Annotated[EmailStr, Field(example="john.doe@example.com")]
    phone: Optional[Annotated[str, Field(max_length=20, example="+1234567890")]] = None

    model_config = ConfigDict(from_attributes=True)
    
    
class UserCreate(UserBase):
    course_id: Annotated[int, Field(ge=1, example=1)]

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: Annotated[int, Field(ge=1, example=1)]
    
class UserDetails(User):
    courses: List[int] = []
