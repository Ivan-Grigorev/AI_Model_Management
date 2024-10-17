# AI Model Management Web Application

A user-friendly web application designed to streamline the management of AI models, datasets, and training processes. Tailored for Japanese employees with basic computer literacy, the application offers an intuitive interface to facilitate efficient AI model management without requiring advanced technical expertise.

## Table of Contents

- [Project Overview](#project-overview)
- [Persona](#persona)
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Directory Structure](#directory-structure)
- [API Routes](#api-routes)
  - [User Routes](#user-routes)
  - [Admin Routes](#admin-routes)
- [Use Cases](#use-cases)
- [Running the Application](#running-the-application)

## Project Overview

This web application facilitates the management of AI models, datasets, and training experiments. It provides functionalities for users to create and manage their accounts, datasets, models, and training processes. Admin users have additional privileges to oversee and manage all aspects of the application, including user management and deletion of datasets and models.

## Persona

**Target User:**  
Japanese employees with basic computer literacy and an understanding of written English. Users are not expected to have prior experience with AI model management, so the user interface is designed to be simple and intuitive to accommodate this demographic.

## Features

- **User Authentication:**
  - Create an account using an email address and password.
  - Secure login and logout functionality.
  
- **Admin Management:**
  - Admin users can log in and out separately.
  - Admins can manage all users, including deleting user accounts.
  - Admins have the authority to delete datasets and models.

- **Dataset and Model Management:**
  - Create, search, and view datasets and models.
  - Admins can view all datasets and models added by any user.
  
- **Training Management:**
  - Launch training sessions by selecting a specific model and dataset.
  - View detailed results of training sessions, including precision and recall percentages.
  
- **Search Functionality:**
  - Search for models, datasets, and trainings by ID or name.
  
- **User Interface:**
  - Available in English to accommodate the target user base.
  - Designed for ease of use with clear navigation and simple forms.

## Technologies

- **Frontend:**  
  Vue.js, Tailwind CSS, Flowbite

- **Backend:**  
  FastAPI (Python 3)

- **Database:**  
  SQLite

- **Deployment:**  
  Docker, Docker Compose

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

### Installation
The application uses environment variables to manage sensitive information and configuration settings. These can be set in the `docker-compose.yml` file.

- `SECRET_KEY`  
  Key used for JWT authentication. Set as SECRET_KEY for development.

- `ADMIN_EMAIL`  
  Email address for the default admin user.

- `ADMIN_PASSWORD`  
  Password for the default admin user.


## Directory Structure
```
├── ai_model_management/
│   └── __init__.py                # Initialization file for the AI model management module
├── backend/
│   ├── Dockerfile                 # Docker configuration for the backend
│   ├── app/                       # Main backend application directory
│   │   ├── __init__.py            # Initialization file for the backend app
│   │   ├── api/
│   │   │   ├── __init__.py                # Initialization file for the API module
│   │   │   ├── admin.py                   # Handles admin-related API routes (e.g., managing users, datasets, and models)
│   │   │   ├── datasets.py                # Manages API routes for dataset creation and retrieval
│   │   │   ├── models.py                  # Manages API routes for model creation and retrieval
│   │   │   ├── trainings.py               # Handles API routes for model training functionality
│   │   │   └── users.py                   # Manages user-related routes like registration, login, etc.
│   │   ├── database/
│   │   │   ├── __init__.py                # Initialization file for database connections
│   │   │   ├── config.py                  # Database configuration settings
│   │   │   └── db_models.py               # Contains database models (tables) for users, datasets, models, etc.
│   │   ├── schemas/
│   │   │   ├── __init__.py                # Initialization file for schemas module
│   │   │   ├── dataset_schemas.py         # Pydantic schemas for validating dataset-related API data
│   │   │   ├── model_schemas.py           # Pydantic schemas for validating model-related API data
│   │   │   ├── training_schemas.py        # Pydantic schemas for validating training-related API data
│   │   │   └── user_schemas.py            # Pydantic schemas for validating user-related API data
│   │   └── main.py                        # Main entry point for the FastAPI backend
│   ├── app.db                     # SQLite database file (for development)
│   ├── .gitignore                 # Git ignore rules for the database directory
│   ├── .gitattributes             # Git attributes configuration file
│   ├── .pre-commit-config.yml     # Pre-commit hooks configuration
├── frontend
│   ├── Dockerfile                 # Configuration for building the frontend Docker image
│   ├── README.md                  # Frontend-specific documentation
│   ├── babel.config.js            # Babel configuration for JavaScript compilation
│   ├── jsconfig.json              # Configuration file for JavaScript tooling
│   ├── node_modules               # Node.js packages and dependencies
│   ├── package-lock.json          # Auto-generated file with versions of installed Node.js packages
│   ├── package.json               # Contains project metadata and Node.js dependencies
│   ├── postcss.config.js          # PostCSS configuration for processing CSS
│   ├── public
│   │   ├── favicon.ico            # Favicon for the application
│   │   ├── index.html             # Main HTML file to mount the Vue.js app
│   ├── src
│   │   ├── App.vue                # Root Vue component that defines the structure of the app
│   │   ├── assets
│   │   │   ├── logo.png               # Logo asset used in the frontend
│   │   │   └── tailwind.css           # Custom styles using TailwindCSS
│   │   ├── components
│   │   │   └── HelloWorld.vue         # Example Vue component (replace or delete in production)
│   │   ├── main.js                    # Entry point for initializing the Vue.js app
│   │   ├── router
│   │   │   └── index.js               # Vue Router setup for managing navigation between views
│   │   ├── services
│   │   │   ├── apiService.js          # Service for handling API requests to the backend
│   │   │   └── authService.js         # Service for handling authentication logic (login, register)
│   │   ├── views
│   │   │   ├── AboutView.vue                # View for displaying information about the app
│   │   │   ├── AdminDatasetDetailsView.vue  # Admin view for dataset details management
│   │   │   ├── AdminDatasetsView.vue        # Admin view for listing and managing datasets
│   │   │   ├── AdminModelDetailsView.vue    # Admin view for model details management
│   │   │   ├── AdminModelsView.vue          # Admin view for listing and managing models
│   │   │   ├── AdminUsersView.vue           # Admin view for managing users
│   │   │   ├── AdminView.vue                # Admin dashboard view
│   │   │   ├── DatasetDetailsView.vue       # User view for dataset details
│   │   │   ├── DatasetView.vue              # User view for listing datasets
│   │   │   ├── HomeView.vue                 # Home page view for the application
│   │   │   ├── LoginView.vue                # View for user login
│   │   │   ├── ModelDetailsView.vue         # User view for model details
│   │   │   ├── ModelView.vue                # User view for listing models
│   │   │   ├── SignUpView.vue               # View for user registration
│   │   │   ├── TrainingDetailsView.vue      # View for viewing training details
│   │   │   ├── TrainingView.vue             # User view for listing training sessions
│   │   │   └── UserView.vue                 # User dashboard view after login
│   ├── tailwind.config.js          # TailwindCSS configuration
│   └── vue.config.js               # Vue.js configuration file for project settings
├── docker-compose.yml              # Docker Compose configuration for orchestrating frontend and backend containers
└── README.md                       # Project documentation
```

## API Routes

### User Routes

- **Home Page**
  - `/`  
    Access the home page of the application.

- **Authentication**
  - `/signin`  
    Register a new user with email and password.
  - `/login`  
    Log in a user with email and password.
  - `/logout`  
    Log out the current user.

- **Dashboard**
  - `/dashboard`  
    Access the user’s dashboard with available functionalities.

- **Datasets Management**
  - `/datasets`  
    Retrieve all datasets.
  - `/datasets`  
    Create a new dataset.
  - `/datasets/{dataset-id}`  
    Retrieve detailed information about a specific dataset.

- **Models Management**
  - `/models`  
    Retrieve all models.
  - `/models`  
    Create a new model.
  - `/models/{model-id}`  
    Retrieve detailed information about a specific model.

- **Trainings Management**
  - `/trainings`  
    Retrieve all training sessions.
  - `/trainings`  
    Launch a new training session.
  - `/trainings/{training-id}`  
    Retrieve detailed information about a specific training session.

### Admin Routes

- **Admin Dashboard**
  - `/admin`  
    Access the admin dashboard with all admin functionalities.

- **User Management**
  - `/admin/users/`  
    Retrieve and manage the list of all users with admin privileges.

- **Datasets Management**
  - `/admin/datasets/`  
    Manage datasets with admin privileges.
  - `/admin/datasets/{dataset-id}`  
    Retrieve detailed information about a specific dataset with admin privileges.

- **Models Management**
  - `/admin/models/`  
    Manage models with admin privileges.
  - `/admin/models/{model-id}`  
    Retrieve detailed information about a specific model with admin privileges.

> **Note:** All functionalities provided by the following routes are available only to authorized users.

## Use Cases

- **User Registration and Authentication:**
  - Users can create an account, log in, and log out seamlessly.
  
- **Dataset Management:**
  - Users can add new datasets by providing a name.
  - View a list of all datasets with clickable IDs to view details.
  - Search datasets by ID or name.

- **Model Management:**
  - Users can create new models by providing a name.
  - View a list of all models with clickable IDs to view details.
  - Search models by ID or name.

- **Training Management:**
  - Users can launch training sessions by specifying an experiment name and selecting one model and one dataset.
  - View detailed results of training sessions, including precision and recall percentages.
  - Search trainings by ID or name.

- **Admin Privileges:**
  - Admins can manage all users, datasets, and models.
  - Admins can delete users, datasets, and models as needed.

## Running the Application

The application is containerized using Docker and orchestrated with Docker Compose to simplify the deployment process. The `docker-compose.yml` file defines the services for the frontend, backend, and database, ensuring that all components run seamlessly together.

1. **Build and Start the Containers:**
   ```bash
   docker-compose up --build
   ```
   This command will automatically install all necessary dependencies for both the frontend and backend.


2. **Access the Application:**
   - **Frontend:** [http://localhost:8080](http://localhost:8080)
   - **Backend API:** [http://localhost:8000](http://localhost:8000)

## License

This project is licensed under the terms of the [LICENSE](./LICENSE).

## Author

This repository was built and is maintained by [Ivan Grigorev](https://github.com/Ivan-Grigorev).

---

Thank you for using the AI Model Management Web Application! We hope it enhances your workflow and makes AI model management effortless.