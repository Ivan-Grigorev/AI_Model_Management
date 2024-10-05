"""Pydantic schemas for user registration and login data validation."""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (str): User's email address.
        password (str): User's password.
    """

    email: EmailStr
    password: str


class UserInDB(UserCreate):
    """
    Schema for returning user data from the database.

    Attributes:
        id (int): Unique identifier for the user.
    """

    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        email (str): User's email address.
        password (str): User's password.
    """

    email: EmailStr
    password: str
