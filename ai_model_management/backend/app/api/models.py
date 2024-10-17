"""API routes for creating, listing, and fetching specific models."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.config import get_db
from ..database.db_models import Model, User
from ..schemas.model_schemas import ModelCreate, ModelResponse
from .users import get_current_user

router = APIRouter()


@router.post('/models', response_model=ModelResponse)
def create_model(
    model: ModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new model.

    Attributes:
        model (ModelCreate): An object containing the details of the model to be created.
        db (Session): SQLAlchemy session to access the database.
        current_user (User): The currently authenticated user.

    Returns:
         ModelResponse: The created model.
    """

    new_model = Model(
        name=model.name,
        user_id=current_user.id,
    )
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model


@router.get('/models', response_model=List[ModelResponse])
def list_models(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all models.

    Attributes:
        current_user: The currently authenticated user.

    Returns:
        List of all models in the database.
    """

    models = (
        db.query(Model).filter((Model.user_id == current_user.id) | User.is_admin).join(User).all()
    )

    return models


@router.get('/models/{model_id}', response_model=ModelResponse)
def get_model(
    model_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific model by its ID.

    Attributes:
        model_id (int): The ID of the model to retrieve.
        current_user: The currently authenticated user.

    Returns:
        The model if found.

    Raises:
        HTTP 404 if not found.
    """

    model = (
        db.query(Model)
        .join(User)
        .filter((Model.id == model_id) & ((Model.user_id == current_user.id) | User.is_admin))
        .first()
    )

    if not model:
        raise HTTPException(status_code=404, detail='Model not found')
    return model


# Admin functionality: Endpoints related to administrative tasks


@router.post('/admin/models', response_model=ModelResponse)
def admin_create_model(
    model: ModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new model. Admin access only.

    Attributes:
        model (ModelCreate): An object containing the details of the model to be created.
        db (Session): SQLAlchemy session to access the database.
        current_user (User): The currently authenticated user.

    Returns:
        ModelResponse: The created model.

    Raises:
        HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    return create_model(model=model, db=db, current_user=current_user)


@router.get('/admin/models', response_model=List[ModelResponse])
def admin_list_models(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Get all models. Admin access only.

    Attributes:
        db (Session): SQLAlchemy session to access the database.
        current_user (User): The currently authenticated user.

    Returns:
        List of all models in the database.

    Raises:
        HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    return list_models(db=db, current_user=current_user)


@router.delete('/admin/models/{model_id}', status_code=status.HTTP_200_OK)
def admin_delete_model(
    model_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Delete a model by ID. Admin access only.

    Attributes:
        model_id (int): The identifier of model.
        db (Session): SQLAlchemy database session.
        current_user (User): The currently authenticated user.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTP 403 if user does not have access.
        HTTP 404 If the model is not found.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Model not found')
    db.delete(model)
    db.commit()
    return {'message': f"Model with {model_id} ID deleted successfully"}


@router.get('/admin/models/{model_id}', response_model=ModelResponse)
def admin_get_model(
    model_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific model by its ID. Admin access only.

    Attributes:
        model_id (int): The ID of the model to retrieve.
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

    Returns:
        The model if found.

    Raises:
        HTTP 403 if user does not have access.
        HTTP 404 if model not found.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    return get_model(model_id=model_id, db=db, current_user=current_user)
