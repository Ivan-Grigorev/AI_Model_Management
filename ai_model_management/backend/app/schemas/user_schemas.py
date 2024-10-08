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


class UserInDB(BaseModel):
    """
    Schema for returning user data from the database.

    Attributes:
        id (int): Unique identifier for the user.
        email (str): User's email address.
        registration_date (str): The user registration date.
    """

    id: int
    email: EmailStr
    registration_date: str

    class Config:
        """
        Config class to enable Pydantic to work with ORM objects, allowing
        initialization of the schema from attributes of database models.
        """

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
