from pydantic import BaseModel,EmailStr,Field,FileUrl
from sqlalchemy import Date
from fastapi import UploadFile
from enum import Enum
from typing import Optional
from datetime import datetime



class UserReadSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True



class BooksAddSchema(BaseModel):
    book_name: str
    deadline: int
    motivation: Optional[str] = None

class BooksInfoSchema(BaseModel):
    book_id : int
    book_name: str
    text: str
    motivation: Optional[str] = None
    created_date: datetime
    deadline_date: datetime
    done: bool

class UserReadWithDoneBooksSchema(UserReadSchema):
    done_books: list[BooksInfoSchema]

    class Config:
        from_attributes = True

class BooksInfoWithDeadlineSchema(BooksInfoSchema):
    deadline: int



