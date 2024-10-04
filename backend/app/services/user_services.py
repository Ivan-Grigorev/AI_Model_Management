"""Service functions for user management, including user creation, password hashing, and password verification."""

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.app.models.user_model import User
from backend.app.schemas.user_schemas import UserCreate

# Initialize password hashin context
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    """
    Hash a password for storing.

    Args:
         password (str): Password to hash.

    Returns:
        str: hashed password.
    """
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (UserCreate): User data from request.

    Returns:
        User: The created user object.
    """
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a provided password against a hashed password.

    Args:
        plain_password (str): The password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
