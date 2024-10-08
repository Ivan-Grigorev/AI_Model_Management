"""API routes for creating, listing, and fetching specific trainings."""

import random
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.other_models import Dataset, Model, Training
from ..schemas.training_schemas import TrainingCreate, TrainingResponse

router = APIRouter()


# Route to create a training
@router.post('/trainings', response_model=TrainingResponse)
def create_training(training: TrainingCreate, db: Session = Depends(get_db)):
    """
    Create a new training.

    Attributes:
        training: TrainingCreate object containing the name of the model.

    Returns:
        The created training.
    """

    # Check if the model exists
    model = db.query(Model).filter(Model.id == training.model_id).first()
    if not model:
        raise HTTPException(
            status_code=404, detail=f"The Model with ID {training.model_id} not found"
        )

    # Check if the dataset exists
    dataset = db.query(Dataset).filter(Dataset.id == training.dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=404, detail=f"The Dataset by {training.dataset_id} ID does not exist"
        )

    new_training = Training(
        training_name=training.training_name,
        model_id=training.model_id,
        model_name=model.name,
        dataset_id=training.dataset_id,
        dataset_name=dataset.name,
        precision=random.uniform(0, 1),  # random precision value between 0 and 1
        recall=random.uniform(0, 1),  # random recall value between 0 and 1
        creation_date=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    )
    db.add(new_training)
    db.commit()
    db.refresh(new_training)
    return new_training


# Route to list all trainings
@router.get('/trainings', response_model=List[TrainingResponse])
def list_trainings(db: Session = Depends(get_db)):
    """
    Get all trainings.

    Returns:
        List of all trainings in the database.
    """

    trainings = db.query(Training).all()
    return trainings


# Route to get a specific training by ID
@router.get('/trainings/{training_id}', response_model=TrainingResponse)
def get_training(training_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific training by ID.

    Attributes:
        training_id (int): The ID of the training to retrieve.

    Returns:
        The training if found.

    Raises:
        HTTP 404 if not found.
    """

    training = db.query(Training).filter(Training.id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail='Training not found')
    return training
