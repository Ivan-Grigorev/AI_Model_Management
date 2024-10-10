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
        creation_date (str): The date of model creation.
        user_is_admin (bool): Indicates if the model was created by an admin.
    """

    id: int
    name: str
    creation_date: str
    user_is_admin: bool

    class Config:
        """
        Config class to enable Pydantic to work with ORM objects, allowing
        initialization of the schema from attributes of database models.
        """

        from_attributes = True
