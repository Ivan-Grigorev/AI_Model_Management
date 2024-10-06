"""Defines the structure and schema for tables in the database."""

from sqlalchemy import Column, Integer, String

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
