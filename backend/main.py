"""Main module for the AI Model Management App."""

from fastapi import FastAPI

app = FastAPI()


# Home route to welcome users to the app
@app.get('/home')
def read_home():
    """
    GET /home

    - Return a welcome message to the user.
    - The main entry point for the frontend to fetch the home page content.
    """
    return {'message': 'Welcome to the AI Model Management App!'}
