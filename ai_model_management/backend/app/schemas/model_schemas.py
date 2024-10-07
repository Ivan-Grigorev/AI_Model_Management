"""Pydantic schemas for models."""

from pydantic import BaseModel


class ModelCreate(BaseModel):
    """
    Pydantic schema for creating a new model record.

    Attributes:
        name (str): The name of the model to be created.
    """

    name: str


class ModelResponse(BaseModel):
    """
    Pydantic schema for returning the details of model record in the response.

    Attributes:
        id (int): The unique identifier for the model.
        name (str): The name of the model.
    """

    id: int
    name: str

    class Config:
        """
        Config class to enable Pydantic to work with ORM objects, allowing
        initialization of the schema from attributes of database models.
        """

        from_attributes = True
