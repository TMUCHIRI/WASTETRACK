# Project Overview

This is a Django-based backend for the WasteTrack application. It provides a RESTful API for user authentication (registration and login). The project is configured to use a PostgreSQL database and JWT for authentication.

## Key Technologies

*   **Backend Framework:** Django
*   **API Framework:** Django Rest Framework
*   **Authentication:** JWT (JSON Web Tokens) with `djangorestframework-simplejwt`
*   **Database:** PostgreSQL
*   **CORS:** `django-cors-headers` is used to handle Cross-Origin Resource Sharing.

## Project Structure

*   `waste_backend/`: The main Django project directory.
    *   `settings.py`: Contains the project settings, including database configuration, installed apps, and middleware.
    *   `urls.py`: The root URL configuration for the project.
*   `auth_app/`: A Django app for handling user authentication.
    *   `models.py`: Defines the `CustomUser` model, which allows users to sign up and log in with either a phone number or an email address.
    *   `views.py`: Contains the `RegisterView` and `LoginView` for handling user registration and login.
    *   `serializers.py`: Defines the `RegisterSerializer` and `LoginSerializer` for data validation.
    *   `urls.py`: Contains the URL patterns for the authentication endpoints.
*   `manage.py`: A command-line utility for interacting with the Django project.

# Building and Running

## Prerequisites

*   Python 3
*   pip (Python package installer)
*   PostgreSQL

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(TODO: Create a `requirements.txt` file)*

## Running the Application

1.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

2.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

# Development Conventions

## API Endpoints

*   `auth/register/`: User registration
*   `auth/login/`: User login

## Coding Style

*   The project follows the standard Django coding style.
*   Use a consistent code formatter like Black.

## Testing

*   *(TODO: Add instructions on how to run tests.)*
