"""
Main FastAPI application entry point, including database initialization
and route inclusion for the application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import datasets, models, trainings, users
from .core.database import Base, engine

# Create all tables in database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend to communicate with the backend (CORS settings).
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include routers for users, datasets, models, and trainings
app.include_router(users.router)
app.include_router(datasets.router)
app.include_router(models.router)
app.include_router(trainings.router)


# Home route to welcome users to the app
@app.get('/home')
def read_home():
    """
    The main entry point for the frontend to fetch the home page content.

    Returns:
         A welcome message to the user.
    """
    return {'message': 'Welcome to the AI Model Management App!'}
