"""API endpoint for admin functionalities."""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..api.users import get_current_user
from ..database.config import get_db
from ..database.db_models import Dataset, Model, User
from ..schemas.dataset_schemas import DatasetCreate, DatasetResponse
from ..schemas.model_schemas import ModelCreate, ModelResponse
from ..schemas.user_schemas import UserResponse

# Create an admin router
router = APIRouter()


@router.get('/users', response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a list of all users in the database. Admin access only.

    Attributes:
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

    Returns:
        List of all users with their data.

    Raises:
        HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    users = db.query(User).all()
    return users


@router.post('/users/delete/{email}')
def delete_user(
    email: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Delete a user from the database by email. Admin access only.

    Attributes:
        email (str): Email of the user to be deleted.
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

    Returns:
        dict: A message confirming the user deletion.

    Raises:
        HTTP 403 if user does not have access.
        HTTP 404 if the user with the specific email is not found.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(db_user)
    db.commit()
    return {'message': f"User {email} has been deleted"}


@router.post('/datasets', response_model=DatasetResponse)
def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new dataset. Admin access only.

    Attributes:
        dataset: DatasetCreate object containing the name of the dataset.
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

    Returns:
         The created dataset.

    Raises:
        HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
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
    Get all datasets. Admin access only.

    Attributes:
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

    Returns:
        List of all datasets in the database.

    Raises:
        HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    datasets = db.query(Dataset).all()
    return datasets


@router.delete('/datasets/{dataset_id}', status_code=status.HTTP_200_OK)
def delete_dataset(
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
        HTTP 403 if user does not have access.
        HTTP 404 if the dataset is not found.
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


@router.get('/datasets/{dataset_id}', response_model=DatasetResponse)
def get_dataset(
    dataset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific dataset by its ID. Admin access only.

    Attributes:
        dataset_id (int): The ID of the dataset to retrieve.
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

    Returns:
        The dataset if found.

    Raises:
        HTTP 403 if user does not have access.
        HTTP 404 if dataset not found.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail='Dataset not found')
    return dataset


@router.post('/models', response_model=ModelResponse)
def create_model(
    model: ModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new model. Admin access only.

    Attributes:
        model: ModelCreate object containing the name of the model.
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

    Returns:
        The created model.

    Raises:
        HTTP 403 if user does not have access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges to access this resource',
        )
    new_model = Model(name=model.name, creation_date=datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model


@router.get('/models', response_model=List[ModelResponse])
def list_models(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all models. Admin access only.

    Attributes:
        db (Session): SQLAlchemy session to access the database.
        current_user (dict): The currently authenticated user.

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
    models = db.query(Model).all()
    return models


@router.delete('/models/{model_id}', status_code=status.HTTP_200_OK)
def delete_model(
    model_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Delete a model by ID. Admin access only.

    Attributes:
        model_id (int): The identifier of model.
        db (Session): SQLAlchemy database session.
        current_user (dict): The currently authenticated user.

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


@router.get('/models/{model_id}', response_model=ModelResponse)
def get_model(
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
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail='Model not found')
    return model
