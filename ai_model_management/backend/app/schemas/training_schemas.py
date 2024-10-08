"""Pydantic schemas for trainings."""

from pydantic import BaseModel


class TrainingCreate(BaseModel):
    """
    Pydantic schema for creating a new training record.

    Attributes:
         training_name (str): The name of training to be created.
         model_id (int): The ID of the model used in the training.
         dataset_id (int): The ID of the dataset used in the training.
    """

    training_name: str
    model_id: int
    dataset_id: int


class TrainingResponse(BaseModel):
    """
    Pydantic schema for returning the details of training record in the response.

    Attributes:
         id (int): The unique identifier for the training.
         training_name (str): The name of training to be created.
         model_id (int): The ID of the model used in the training.
         model_name (str): The name of the model used in the training.
         dataset_id (int): The ID of the dataset used in the training.
         dataset_name (str): The name of the dataset used in the training.
         precision (float): The precision value for the training results.
         recall (float): The recall value for the training results.
         creation_date (str): The date of training creation.
    """

    id: int
    training_name: str
    model_id: int
    model_name: str
    dataset_id: int
    dataset_name: str
    precision: float
    recall: float
    creation_date: str

    class Config:
        """
        Config class to enable Pydantic to work with ORM objects, allowing
        initialization of the schema from attributes of database models.
        """

        from_attributes = True
