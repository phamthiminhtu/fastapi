from pydantic import BaseModel, Field
from pydantic import field_validator
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, Depends


class Address(BaseModel):
    city: str
    zipcode: str

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    min_age: Optional[int] = None
    role: Optional[str] = None
    address: Address = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("name")
    @classmethod
    def name_must_be_long(cls, value):
        if len(value) < 3:
            raise ValueError("Name too short")
        return value

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, value):
        if "@" not in value:
            raise ValueError("Invalid email")
        return value

# user = User(id=1, name="Tom", email="tom@example.com", age=30, address=Address(city="New York", zipcode="10001"))
# print(user.created_at)

class UserCreate(User):
    password: str = None
    response_message: str = None

    class Config:
        from_attributes = True

    def model_post_init(self, __context):
        self.response_message = f"User {self.id} created"

class UserPublic(UserCreate):
    password: str = Field(default=None, exclude=True)

    class Config:
        from_attributes = True

