"""API routes for creating, listing, and fetching specific datasets."""

from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.other_models import Dataset
from ..schemas.dataset_schemas import DatasetCreate, DatasetResponse

router = APIRouter()


# Route to create a dataset
@router.post('/datasets', response_model=DatasetResponse)
def create_dataset(dataset: DatasetCreate, db: Session = Depends(get_db)):
    """
    Create a new dataset.

    Attributes:
        dataset: DatasetCreate object containing the name of the dataset.

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


# Route to list all datasets
@router.get('/datasets', response_model=List[DatasetResponse])
def list_datasets(db: Session = Depends(get_db)):
    """
    Get all datasets.

    Returns:
        List all datasets in the database.
    """

    datasets = db.query(Dataset).all()
    return datasets


# Route to get a specific dataset by ID
@router.get('/datasets/{dataset_id}', response_model=DatasetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific dataset by its ID.

    Attributes:
        dataset_id (int): The ID of the dataset to retrieve.

    Returns:
         The dataset if found.

     Raises:
         HTTP 404 if not found.
    """

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail='Dataset not found')
    return dataset
