"""API routes for creating, listing, and fetching specific datasets."""

from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..models.other_models import Dataset
from ..schemas.dataset_schemas import DatasetCreate, DatasetResponse

router = APIRouter()


# Route to create a dataset
@router.post('/datasets', response_model=DatasetResponse)
def create_dataset(dataset: DatasetCreate):
    """
    Create a new dataset.

    Attributes:
        dataset: DatasetCreate object containing the name of the dataset.

    Returns:
         The created dataset.
    """
    db: Session = SessionLocal()
    new_dataset = Dataset(name=dataset.name)
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    return new_dataset


# Route to list all datasets
@router.get('/datasets', response_model=List[DatasetResponse])
def list_datasets():
    """
    Get all datasets.

    Returns:
        List all datasets in the database.
    """
    db: Session = SessionLocal()
    datasets = db.query(Dataset).all()
    return datasets


# Route to get a specific dataset by ID
@router.get('/datasets/{dataset_id}', response_model=DatasetResponse)
def get_dataset(dataset_id: int):
    """
    Retrieve a specific dataset by its ID.

    Attributes:
        dataset_id (int): The ID of the dataset to retrieve.

    Returns:
         The dataset if found.

     Raises:
         HTTP 404 if not found.
    """
    db: Session = SessionLocal()
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail='Dataset not found')
    return dataset
