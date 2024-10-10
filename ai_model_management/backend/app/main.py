"""
Main FastAPI application entry point, including database initialization
and route inclusion for the application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import admin, datasets, models, trainings, users
from .api.users import register_admin
from .database.config import Base, SessionLocal, engine

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

# Include routers
app.include_router(admin.router, prefix='/admin')
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


def startup_event():
    """
    Create a new database session and register the admin user.
    """
    db = SessionLocal()
    register_admin(db)
    db.close()


# Register the startup event handler
app.add_event_handler('startup', startup_event)
