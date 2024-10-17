"""API routes for creating, listing, and fetching specific datasets."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.config import get_db
from ..database.db_models import Dataset, User
from ..schemas.dataset_schemas import DatasetCreate, DatasetResponse
from .users import get_current_user

router = APIRouter()


@router.post('/datasets', response_model=DatasetResponse)
def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new dataset.

    Attributes:
        dataset (DatasetCreate): An object containing the details of the dataset to be created.
        db (Session): SQLAlchemy session to access the database.
        current_user (User): The currently authenticated user.

    Returns:
         DatasetResponse: The created dataset.
    """

    new_dataset = Dataset(
        name=dataset.name,
        user_id=current_user.id,
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
        db (Session): SQLAlchemy session to access the database.
        current_user (User): The currently authenticated user.

    Returns:
        List of all datasets in the database.
    """

    datasets = (
        db.query(Dataset)
        .filter((Dataset.user_id == current_user.id) | User.is_admin)
        .join(User)
        .all()
    )

    return datasets


@router.get('/datasets/{dataset_id}', response_model=DatasetResponse)
def get_dataset(
    dataset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific dataset by its ID.

    Attributes:
        dataset_id (int): The ID of the dataset to retrieve.
        db (Session): SQLAlchemy session to access the database.
        current_user (User): The currently authenticated user.

    Returns:
         DatasetResponse: The dataset if found.

     Raises:
         HTTPException: HTTP 404 if dataset not found.
    """

    dataset = (
        db.query(Dataset)
        .join(User)
        .filter((Dataset.id == dataset_id) & ((Dataset.user_id == current_user.id) | User.is_admin))
        .first()
    )
    if not dataset:
        raise HTTPException(status_code=404, detail='Dataset not found')
    return dataset


# Admin functionality: Endpoints related to administrative tasks


@router.post('/admin/datasets', response_model=DatasetResponse)
def admin_create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new dataset. Admin access only.

    Attributes:
        dataset (DatasetCreate): An object containing the details of the dataset to be created.
        db (Session): SQLAlchemy session to access the database.
        current_user (User): The currently authenticated user.

    Returns:
         DatasetResponse: The created dataset.

    Raises:
        HTTPException: HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    return create_dataset(dataset=dataset, db=db, current_user=current_user)


@router.get('/admin/datasets', response_model=List[DatasetResponse])
def admin_list_datasets(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Get all datasets. Admin access only.

    Attributes:
        db (Session): SQLAlchemy session to access the database.
        current_user (User): The currently authenticated user.

    Returns:
        List of all datasets in the database.

    Raises:
        HTTPException: HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    return list_datasets(db=db, current_user=current_user)


@router.delete('/admin/datasets/{dataset_id}', status_code=status.HTTP_200_OK)
def admin_delete_dataset(
    dataset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Delete a dataset by ID. Admin access only.

    Attributes:
        dataset_id (int): The identifier of dataset.
        db (Session): SQLAlchemy database session.
        current_user (dict): The currently authenticated user.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: HTTP 403 if user does not have access.
        HTTPException: HTTP 404 if the dataset is not found.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dataset not found')

    db.delete(dataset)
    db.commit()
    return {'message': f"Dataset with {dataset_id} ID deleted successfully"}


@router.get('/admin/datasets/{dataset_id}', response_model=DatasetResponse)
def admin_get_dataset(
    dataset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific dataset by its ID. Admin access only.

    Attributes:
        dataset_id (int): The ID of the dataset to retrieve.
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

    Returns:
        DatasetResponse: The dataset if found.

    Raises:
        HTTPException: HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    return get_dataset(dataset_id=dataset_id, db=db, current_user=current_user)
