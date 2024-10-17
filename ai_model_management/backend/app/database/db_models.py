"""Defines the structure for tables in the database."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from .config import Base


class User(Base):
    """
    User model for storing user data.

    Attributes:
        id (int): Unique identifier for the user.
        email (str): User's email address (used for login).
        hashed_password (str): User's hashed password for authentication.
        registration_date (str): The User's registration date.
        is_admin (bool): Flag indicating if the user is an admin.

    Relationship:
        datasets: A one-to-many relationship with Dataset table,
                representing all datasets created by this user.
        models: A one-to-many relationship with the Model table,
                representing all models created byt his user.
        trainings: A one-to-many relationship with the Training table,
                representing all trainings created byt this user.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    registration_date = Column(String, default=datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    is_admin = Column(Boolean, default=False)

    datasets = relationship('Dataset', back_populates='owner')
    models = relationship('Model', back_populates='owner')
    trainings = relationship('Training', back_populates='owner')


class Dataset(Base):
    """
    Represent a Dataset in the database.

    Attributes:
        id (int): A unique identifier for the dataset (primary key).
        name (str): The name of the dataset.
        creation_date (str): The creation date of dataset.
        user_id (int): The ID of the user who created this dataset.

    Relationships:
        owner: A many-to-one relationship wih the User table,
                linking this dataset to the user who created it.
        trainings: A one-to-many relationship with the Training table,
                representing all training experiments that use this dataset.
    """

    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    creation_date = Column(String, default=datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='datasets')
    trainings = relationship('Training', back_populates='dataset')


class Model(Base):
    """
    Represent a Model in the database.

    Attributes:
        id (int): A unique identifier for the model (primary key).
        name (str): The name of the model.
        creation_date (str): The creation date of model.
        user_id (int): The ID of the user who created this model.

    Relationships:
        owner: A many-to-one relationship with the User table,
                linking this model to the user created it.
        trainings: A one-to-many relationship with the Training table,
                representing all training experiments that use this model.
    """

    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    creation_date = Column(String, default=datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='models')
    trainings = relationship('Training', back_populates='model')


class Training(Base):
    """
    Represent a Training in the database.

    Attributes:
        id (int): A unique identifier for the training (primary key).
        training_name (str): The name of the training.
        model_id (int): The ID of the model used in the training.
        model_name (str): The name of the model used in the training.
        dataset_id (int): The ID of the dataset used in the training.
        dataset_name (str): The name of the dataset used in the training.
        precision (float): The precision value for the training results.
        recall (float): The recall value for the training results.
        creation_date (str): The creation date of the experiment.
        user_id (int): The ID of the user who conducted this training.

    Relationships:
        model: A many-to-one relationship with the Model table,
                linking this training to a specific model.
        dataset: A many-to-one relationship with the Dataset table,
                linking this training to a specific dataset.
        owner: A many-to-one relationship with the User table,
                linking this training to the user who conducted it.
    """

    __tablename__ = 'trainings'

    id = Column(Integer, primary_key=True, index=True)
    training_name = Column(String, nullable=False)
    model_id = Column(Integer, ForeignKey('models.id'))
    model_name = Column(String)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    dataset_name = Column(String)
    precision = Column(Float)
    recall = Column(Float)
    creation_date = Column(String, default=datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    user_id = Column(Integer, ForeignKey('users.id'))

    model = relationship('Model', back_populates='trainings')
    dataset = relationship('Dataset', back_populates='trainings')
    owner = relationship('User', back_populates='trainings')
