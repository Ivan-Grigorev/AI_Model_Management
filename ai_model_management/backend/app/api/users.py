"""User management module."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime

from ..database.config import get_db
from ..database.db_models import User
from ..schemas.user_schemas import UserInDB, UserCreate

# Create a router for user-related routes
router = APIRouter()

# Use OAuth2PasswordBearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Initialize password hashing context
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by checking their email and password.

    Attributes:
        db (Session): SQLAlchemy session to access the database.
        email (str): User's email address.
        password (str): User's password.

    Returns:
        User: The authenticated user if the credentials are valid, otherwise None.
    """
    user = db.query(User).filter(User.email == email).first()
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None


@router.post('/signin', response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    User registration endpoint.

    Attributes:
        user (UserCreate): User data for registration.
        db (Session): SQLAlchemy database session.

    Returns:
        UserInDB: The created user object.

    Raises:
        HTTPException: If the email is already registered.
    """
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered'
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        registration_date=datetime.now().date().strftime('%Y/%m/%d')
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post('/login', response_model=dict)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login endpoint.

    Attributes:
        form_data (OAuth2PasswordRequestForm): User credential for login.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing access token and redirect URL if applicable.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # Check if the user is an admin
    if user.is_admin:
        return {'access_token': user.email, 'token_type': 'bearer', 'redirect_url': '/admin/'}

    return {'access_token': user.email, 'token_type': 'bearer'}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the currently authenticated user based on their token.

    Attributes:
        token (str): The OAuth2 token for the current session.
        db (Session): SQLAlchemy session to access the database.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    user = db.query(User).filter(User.email == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    return user


def get_current_admin(user: User = Depends(get_current_user)):
    """
    Ensure the current user is admin.

    Attributes:
        user (User): The currently authenticated user.

    Returns:
        User: The authenticated admin user.

    Raises:
        HTTPException: If the user is not admin.
    """
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough privileges')
    return user
