"""
Main FastAPI application entry point, including database initialization
and route inclusion for the application.
"""

from fastapi import FastAPI

from .api import users
from .core.database import engine, Base


# Create all tables in database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the user router
app.include_router(users.router, prefix='/api/users')


# Home route to welcome users to the app
@app.get('/home')
def read_home():
    """
    GET /home

    - Return a welcome message to the user.
    - The main entry point for the frontend to fetch the home page content.
    """
    return {'message': 'Welcome to the AI Model Management App!'}
