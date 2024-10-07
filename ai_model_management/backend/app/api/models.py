"""API routes for creating, listing, and fetching specific models."""

from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..models.other_models import Model
from ..schemas.model_schemas import ModelCreate, ModelResponse

router = APIRouter()


# Route to create a model
@router.post('/models', response_model=ModelResponse)
def create_model(model: ModelCreate):
    """
    Create a new model.

    Attributes:
        model: ModelCreate object containing the name of the model.

    Returns:
        The created model.
    """

    db: Session = SessionLocal()
    new_model = Model(name=model.name)
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model


# Route to list all models
@router.get('/models', response_model=List[ModelResponse])
def list_models():
    """
    Get all models.

    Returns:
        List of all models in the database.
    """
    db: Session = SessionLocal()
    models = db.query(Model).all()
    return models


# Router to get a specific model by ID
@router.get('/models/{model_id}', response_model=ModelResponse)
def get_model(model_id: int):
    """
    Retrieve a specific model by its ID.

    Attributes:
        model_id (int): The ID of the model to retrieve.

    Returns:
        The model if found.

    Raises:
        HTTP 404 if not found.
    """

    db: Session = SessionLocal()
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail='Model not found')
    return model
