"""Defines the structure and schema for tables in the database."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base


class Dataset(Base):
    """
    Represent a Dataset in the database.

    Attributes:
        id: A unique identifier for the dataset (primary key).
        name: The name of the dataset.
    """

    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    trainings = relationship('Training', back_populates='dataset')


class Model(Base):
    """
    Represent a Model in the database.

    Attributes:
        id: A unique identifier for the model (primary key).
        name: The name of the model.
    """

    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    trainings = relationship('Training', back_populates='model')


class Training(Base):
    """
    Represent a Training in the database.

    Attributes:
        id: A unique identifier for the training (primary key).
        experiment_name: The name of experiment.
        model_id: The ID of the model used in the training.
        model_name: The name of the model used in the training.
        dataset_id: The ID of the dataset used in the training.
        dataset_name: The name of the dataset used in the training.
        precision: The precision value for the training results.
        recall: The recall value for the training results.
    """

    __tablename__ = 'trainings'

    id = Column(Integer, primary_key=True, index=True)
    experiment_name = Column(String, nullable=False)
    model_id = Column(Integer, ForeignKey('models.id'))
    model_name = Column(String)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    dataset_name = Column(String)
    precision = Column(Float)
    recall = Column(Float)

    model = relationship('Model', back_populates='trainings')
    dataset = relationship('Dataset', back_populates='trainings')
