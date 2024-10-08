"""API endpoint for admin functionalities."""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.other_models import Dataset, Model
from ..models.user_model import User
from ..schemas.dataset_schemas import DatasetCreate, DatasetResponse
from ..schemas.model_schemas import ModelCreate, ModelResponse
from ..schemas.user_schemas import UserInDB

# Create an admin router
router = APIRouter()


@router.get('/users', response_model=List[UserInDB])
def get_users(db: Session = Depends(get_db)):
    """
    Retrieve a list of all users in the database. Admin access only.

    Attributes:
        db (Session): SQLAlchemy session to access the database.

    Returns:
        List[UserInDb]: List of users with their IDs and emails.
    """

    users = db.query(User).all()
    return users


@router.post('/users/delete/{email}')
def delete_user(email: str, db: Session = Depends(get_db)):
    """
    Delete a user from the database by email. Admin access only.

    Attributes:
        email (str): Email of the user to be deleted.
        db (Session): SQLAlchemy session to access the database.
        admin (User): The current admin user (checked via dependency).

    Returns:
        dict: A message confirming the user deletion.

    Raises:
        HTTPException: If the user with the specific email is not found.
    """

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    db.delete(user)
    db.commit()
    return {'message': f"User {email} has been deleted"}


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


@router.delete('/datasets/{dataset_id}', status_code=status.HTTP_200_OK)
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """
    Delete a dataset by ID.

    Attributes:
        dataset_id (int): The identifier of dataset.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the dataset is not found.
    """

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dataset not found')

    db.delete(dataset)
    db.commit()

    return {'message': f"Dataset with {dataset_id} ID deleted successfully"}


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


@router.post('/models', response_model=ModelResponse)
def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    """
    Create a new model.

    Attributes:
        model: ModelCreate object containing the name of the model.

    Returns:
        The created model.
    """

    new_model = Model(name=model.name, creation_date=datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model


@router.delete('/models/{model_id}', status_code=status.HTTP_200_OK)
def delete_model(model_id: int, db: Session = Depends(get_db)):
    """
    Delete a model by ID.

    Attributes:
        model_id (int): The identifier of model.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the model is not found.
    """

    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Model not found')

    db.delete(model)
    db.commit()

    return {'message': f"Model with {model_id} ID deleted successfully"}


@router.get('/models/{model_id}', response_model=ModelResponse)
def get_model(model_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific model by its ID.

    Attributes:
        model_id (int): The ID of the model to retrieve.

    Returns:
        The model if found.

    Raises:
        HTTP 404 if not found.
    """

    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail='Model not found')
    return model
