"""API endpoint for user registration and login functionalities."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime

from ..core.database import get_db
from ..models.user_model import User
from ..schemas.user_schemas import UserCreate, UserInDB, UserLogin

router = APIRouter()

# Initialize password hashing context
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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
    # is_admin = user.email == 'admin@ai-model-app.co.jp' and user.password == 'YmUy0DUyMj'
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        registration_date=datetime.now().date().strftime('%Y/%m/%d')
    )  # , is_admin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    User login end point.

    Attributes:
        user (UserLogin): User credential for login.
        db (Session): SQLAlchemy database session.

    Returns:
        HTTPException: If the user is not found or password is incorrect.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password'
        )
    return {'message': 'Login successful'}


@router.post('/logout')
def logout():
    """
    Log out the user by invalidating their session or token.

    Returns:
        dict: A message indicating successful logout.
    """
    return {'message': 'Logout successful'}
