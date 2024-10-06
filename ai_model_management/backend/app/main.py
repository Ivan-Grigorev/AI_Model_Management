"""
Main FastAPI application entry point, including database initialization
and route inclusion for the application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import users, datasets, models
from .core.database import engine, Base


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

# Include routers for users, datasets, and models
app.include_router(users.router)
app.include_router(datasets.router)
app.include_router(models.router)


# Home route to welcome users to the app
@app.get('/home')
def read_home():
    """
    GET /home

    - Return a welcome message to the user.
    - The main entry point for the frontend to fetch the home page content.
    """
    return {'message': 'Welcome to the AI Model Management App!'}
