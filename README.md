# Parking Recommendation API

This project is a FastAPI-based application that provides parking recommendations based on a user's work location and preferred entrance. It is designed to be a starting point for a more complex parking guidance system.

## Features

-   **FastAPI Backend**: A modern, fast (high-performance) web framework for building APIs with Python.
-   **Automatic API Documentation**: Interactive API documentation (Swagger UI) is automatically generated.
-   **In-Memory Database**: Uses an in-memory SQLite database for easy setup and testing, managed with SQLAlchemy.
-   **Structured Project**: The project is split into modules for better organization and maintainability.
-   **Database Initialization**: Supports loading an `init.sql` file on startup to create tables and populate initial data.

## Tech Stack

-   [FastAPI](https://fastapi.tiangolo.com/): The web framework.
-   [Uvicorn](https://www.uvicorn.org/): The ASGI server to run the application.
-   [Pydantic](https://pydantic-docs.helpmanual.io/): For data validation and settings management.
-   [SQLAlchemy](https://www.sqlalchemy.org/): For database interaction (ORM).

## Prerequisites

-   Python 3.8+
-   `pip` for package installation

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To start the API server, run the following command in the root directory of the project:

```bash
uvicorn main:app --reload
```

The server will start, and the API will be accessible at `http://127.0.0.1:8000`. The `--reload` flag makes the server restart automatically after code changes.

## API Documentation (Swagger UI)

Once the application is running, you can access the interactive API documentation in your browser at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

This interface allows you to see all the available endpoints, their request/response models, and test them directly.

The main endpoint is:
- `POST /api/v1/parking/recommendation`

## Project Structure

The project follows a structured layout to separate concerns:

```
.
├── api/
│   └── v1/
│       └── endpoints/
│           └── parking.py      # API endpoint for parking
├── crud.py                     # Database Create, Read, Update, Delete functions
├── database.py                 # Database connection and session setup
├── main.py                     # Main application entry point
├── models.py                   # SQLAlchemy database models (tables)
├── requirements.txt            # Project dependencies
├── schemas.py                  # Pydantic models (API data shapes)
└── init.sql                    # (Optional) SQL script for DB initialization
```

## Database

The application uses an in-memory SQLite database, which is created and destroyed on every application run.

To initialize the database with your own tables and data, create an `init.sql` file in the root directory. This file will be automatically executed when the application starts. 