"""API routes for creating, listing, and fetching specific datasets."""

from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.config import get_db
from ..database.db_models import User, Dataset
from ..schemas.dataset_schemas import DatasetCreate, DatasetResponse
from .users import get_current_user

router = APIRouter()


@router.post('/datasets', response_model=DatasetResponse)
def create_dataset(
        dataset: DatasetCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Create a new dataset.

    Attributes:
        dataset: DatasetCreate object containing the name of the dataset.
        current_user: The currently authenticated user.

    Returns:
         The created dataset.
    """

    new_dataset = Dataset(
        name=dataset.name, creation_date=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    )
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    return new_dataset


@router.get('/datasets', response_model=List[DatasetResponse])
def list_datasets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all datasets.

    Attributes:
        current_user: The currently authenticated user.

    Returns:
        List all datasets in the database.
    """

    datasets = db.query(Dataset).all()
    return datasets


@router.get('/datasets/{dataset_id}', response_model=DatasetResponse)
def get_dataset(
        dataset_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific dataset by its ID.

    Attributes:
        dataset_id (int): The ID of the dataset to retrieve.
        current_user: The currently authenticated user.

    Returns:
         The dataset if found.

     Raises:
         HTTP 404 if not found.
    """

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail='Dataset not found')
    return dataset
