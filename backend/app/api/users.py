"""API endpoint for user registration and login functionalities."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.user_model import User
from backend.app.schemas.user_schemas import UserCreate, UserInDB, UserLogin
from backend.app.services.user_services import create_user, verify_password

router = APIRouter()


@router.post('/signin', response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    User registration endpoint.

    Args:
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
    return create_user(db=db, user=user)


@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    User login end point.

    Args:
        user (UserLogin): User credential for login.
        db (Session): SQLAlchemy database session.

    Returns:
        HTTPException: If the user is not found or password is incorrect.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
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
