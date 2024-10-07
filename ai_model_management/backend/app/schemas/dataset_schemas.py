"""Pydantic schemas for datasets."""

from pydantic import BaseModel


class DatasetCreate(BaseModel):
    """
    Pydantic schema for creating a new dataset record.

    Attributes:
        name (str): The name of the dataset to be created.
    """

    name: str


class DatasetResponse(BaseModel):
    """
    Pydantic schema for returning the details of dataset record in the response.

    Attributes:
        id (int): The unique identifier for the dataset.
        name (str): The name of the dataset.
    """

    id: int
    name: str

    class Config:
        """
        Config class to enable Pydantic to work with ORM objects, allowing
        initialization of the schema from attributes of database models.
        """

        from_attributes = True
