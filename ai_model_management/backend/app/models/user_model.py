"""User model for storing user data in the database."""

from sqlalchemy import Column, Integer, String, Boolean

from ..core.database import Base


class User(Base):
    """
    User model for storing user data.

    Attributes:
        id (int): Unique identifier for the user.
        email (str): User's email address (used for login).
        hashed_password (str): User's hashed password for authentication.
        registration_date (str): The User's registration date.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    registration_date = Column(String)
