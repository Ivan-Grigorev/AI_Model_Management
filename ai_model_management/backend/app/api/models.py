"""API routes for creating, listing, and fetching specific models."""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
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
        model: ModelCreate object containing the name of the model.

    Returns:
        The created model.
    """

    new_model = Model(
        name=model.name,
        creation_date=datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
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

    models = db.query(Model).filter(Model.user_id == current_user.id).all()
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
        db.query(Model).filter((Model.id == model_id) & (Model.user_id == current_user.id)).first()
    )
    if not model:
        raise HTTPException(status_code=404, detail='Model not found')
    return model
