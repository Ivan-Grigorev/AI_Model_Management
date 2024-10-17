"""API routes for creating, listing, and fetching specific trainings."""

import random
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.config import get_db
from ..database.db_models import Dataset, Model, Training, User
from ..schemas.training_schemas import TrainingCreate, TrainingResponse
from .users import get_current_user

router = APIRouter()


@router.post('/trainings', response_model=TrainingResponse)
def create_training(
    training: TrainingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new training.

    Attributes:
        training: TrainingCreate object containing the name of the model.
        current_user: The currently authenticated user.

    Returns:
        The created training.
    """

    # Check if the model created by the current user or admin exists
    model = (
        db.query(Model)
        .join(User)
        .filter(
            (Model.id == training.model_id) & ((Model.user_id == current_user.id) | User.is_admin)
        )
        .first()
    )
    if not model:
        raise HTTPException(
            status_code=404, detail=f"The Model with ID {training.model_id} not found"
        )

    # Check if the dataset created by the current user or admin exists
    dataset = (
        db.query(Dataset)
        .join(User)
        .filter(
            (Dataset.id == training.dataset_id)
            & ((Dataset.user_id == current_user.id) | User.is_admin)
        )
        .first()
    )
    if not dataset:
        raise HTTPException(
            status_code=404, detail=f"The Dataset with ID {training.dataset_id} not found"
        )

    new_training = Training(
        training_name=training.training_name,
        model_id=training.model_id,
        model_name=model.name,
        dataset_id=training.dataset_id,
        dataset_name=dataset.name,
        precision=random.uniform(0, 1),  # random precision value between 0 and 1
        recall=random.uniform(0, 1),  # random recall value between 0 and 1
        user_id=current_user.id,
    )
    db.add(new_training)
    db.commit()
    db.refresh(new_training)
    return new_training


@router.get('/trainings', response_model=List[TrainingResponse])
def list_trainings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all trainings.

    Returns:
        List of all trainings in the database.
    """

    trainings = db.query(Training).filter(Training.user_id == current_user.id).all()
    return trainings


@router.get('/trainings/{training_id}', response_model=TrainingResponse)
def get_training(
    training_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific training by ID.

    Attributes:
        training_id (int): The ID of the training to retrieve.
        current_user: The currently authenticated user.

    Returns:
        The training if found.

    Raises:
        HTTP 404 if not found.
    """

    training = (
        db.query(Training)
        .filter((Training.id == training_id) & (Training.user_id == current_user.id))
        .first()
    )
    if not training:
        raise HTTPException(status_code=404, detail='Training not found')
    return training
