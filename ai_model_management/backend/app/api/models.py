"""Models API for creating, listing, and fetching specific models."""

from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..models.other_models import Model

router = APIRouter()


class ModelCreate(BaseModel):
    """
    Pydantic model for model creation.

    Attributes:
        name (str): The name of the model to be created.
    """

    name: str


class ModelResponse(BaseModel):
    """
    Response model for models.

    Attributes:
        id (int): The unique identifier from the model.
        name (str): The name of the model.
    """

    id: int
    name: str

    class Config:
        """
        Allow the model to initialize from attributes
        instead of just keywords arguments.
        """

        from_attributes = True


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
@router.get('/models', response_model=List[ModelCreate])
def list_models():
    """
    GET all models.

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
