"""Pydantic schemas for user registration and login data validation."""

from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for returning authentication tokens.

    Attributes:
        access_token (str): The JWT access token for the user.
        token_type (str): The type of the token (e.g., 'bearer').
        redirect_url (str | None): Optional URL to redirect after successful login.
    """

    access_token: str
    token_type: str
    redirect_url: str | None = None


class TokenData(BaseModel):
    """
    Schema for the data extracted from the JWT token.

    Attributes:
        email (str | None): The email of the user associated with the token.
    """

    email: str | None = None


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (str): User's email address.
        password (str): User's password.
    """

    email: str
    password: str


class UserInDB(UserCreate):
    """
    Schema for returning user data from the database.

    Attributes:
        hashed_password (str): The hashed password of the user.
    """

    hashed_password: str

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

    email: str
    password: str
