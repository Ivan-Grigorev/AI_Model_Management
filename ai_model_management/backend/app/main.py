"""
Main FastAPI application entry point, including database initialization
and route inclusion for the application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import users
from .core.database import engine, Base


# Create all tables in database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend to communicate with the backend (CORS settings).
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include the user router
app.include_router(users.router)


# Home route to welcome users to the app
@app.get('/home')
def read_home():
    """
    GET /home

    - Return a welcome message to the user.
    - The main entry point for the frontend to fetch the home page content.
    """
    return {'message': 'Welcome to the AI Model Management App!'}
