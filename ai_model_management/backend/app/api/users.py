"""User management module with JWT authentication."""

import os
from datetime import datetime, timedelta
from typing import Annotated, Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database.config import get_db
from ..database.db_models import User
from ..schemas.user_schemas import Token, TokenData, UserCreate, UserLogin

# Create a router for user-related routes
router = APIRouter()

# Use OAuth2PasswordBearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Initialize password hashing context
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# JWT configuration
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieve the currently authenticated user based on the provided JWT token.

    Attributes:
        token (str): JWT token passed through the request header.
        db (Session): SQLAlchemy session object for database access.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(token_data.email, db)
    if user is None:
        raise credentials_exception
    return user


def verify_password(plain_password, hashed_password):
    """
    Verify that a plain password matches its hashed equivalent.

    Attributes:
        plain_password (str): The plain text password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash a plain text password.

    Attributes:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.

    Attributes:
        data (dict): The data to encode into the JWT token.
        expires_delta (Optional[timedelta]): The expiration time for the token. If not provided, defaults to 30 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(email: str, db: Session = Depends(get_db)):
    """
    Retrieve a user from the database by email.

    Attributes:
        email (str): The email of the user to retrieve.
        db (Session): SQLAlchemy session object for database access.

    Returns:
        User: The user object if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    """
    Authenticate a user by verifying their email and password.

    Attributes:
        email (str): The user's email.
        password (str): The user's plain text password.
        db (Session): SQLAlchemy session object for database access.

    Returns:
        User: The authenticated user object if authentication is successful, False otherwise.
    """
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post('/signin', response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    User registration endpoint. Creates a new user account and returns a JWT token.

    Attributes:
        user (UserCreate): The user details provided in the request body.
        db (Session): SQLAlchemy session object for database access.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the email is already registered.
    """
    existing_user = get_user(user.email, db)
    if existing_user:
        raise (
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered'
            )
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        registration_date=datetime.now().date().strftime('%Y/%m/%d'),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={'sub': db_user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/token', response_model=Token)
async def login_for_access_token(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint. Authenticates a user and returns a JWT token.

    Attributes:
        user_login (UserLogin): The user's login credentials (email and password).
        db (Session): SQLAlchemy session object for database access.

    Returns:
        dict: A dictionary containing the access token, token type, and redirect URL.

    Raises:
        HTTPException: If authentication fails.
    """
    user = authenticate_user(user_login.email, user_login.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(data={"sub": user.email})

    if user.is_admin:
        return {'access_token': access_token, 'token_type': 'bearer', 'redirect_url': '/admin'}

    return {'access_token': access_token, 'token_type': 'bearer', 'redirect_url': '/dashboard'}


@router.get('/users/me', response_model=UserCreate)
async def read_users_me(current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Retrieve the details of the currently authenticated user.

    Attributes:
        current_user (dict): The currently authenticated user's details.

    Returns:
        dict: The authenticated user's details.
    """
    return current_user


def register_admin(db: Session = Depends(get_db)):
    """
    Admin registration endpoint. Creates an admin account and returns a JWT token.

    Attributes:
        db (Session): SQLAlchemy session object for database access.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTP 500 If the admin credentials are not set in environment variables.
    """
    # Get admin credentials from environment variables
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')

    if not admin_email or not admin_password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Admin credentials are not set in environment variables',
        )

    existing_admin = get_user(admin_email, db)
    if existing_admin:
        return {'message': 'Admin already exists'}

    hashed_password = get_password_hash(admin_password)
    db_admin = User(
        email=admin_email,
        hashed_password=hashed_password,
        registration_date=datetime.now().date().strftime('%Y/%m/%d'),
        is_admin=True,
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    access_token = create_access_token(data={'sub': db_admin.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
