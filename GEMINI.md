# Project Overview

This is a monorepo for the WasteTrack application, consisting of a Django-based backend and an Angular-based frontend. The application aims to provide a platform for reporting and managing waste.

## Backend (Django)

### Project Overview

The backend is a Django REST API that provides functionalities for user authentication (registration and login) and waste reporting. It uses JWT for authentication and PostgreSQL as its database. CORS is configured to allow requests from the Angular frontend.

### Key Technologies

*   **Framework:** Django, Django REST Framework
*   **Authentication:** JWT (djangorestframework-simplejwt)
*   **Database:** PostgreSQL
*   **CORS:** django-cors-headers

### API Endpoints (Inferred)

*   `/admin/`: Django Admin interface
*   `/auth/register/`: User registration
*   `/auth/login/`: User login
*   `/api/reports/`: Waste reporting functionalities

### Building and Running

1.  **Navigate to the backend directory:**
    ```bash
    cd BACKEND/waste_backend
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```
4.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The backend will be available at `http://127.0.0.1:8000`.

## Frontend (Angular)

### Project Overview

The frontend is an Angular application that provides the user interface for WasteTrack. It allows users to register, log in, report waste, and view existing reports. It utilizes Angular Material for UI components and Angular Google Maps for map functionalities.

### Key Technologies

*   **Framework:** Angular
*   **UI Components:** Angular Material
*   **Mapping:** Angular Google Maps

### Key Routes

*   `/landing`: Landing page
*   `/login`: User login page
*   `/register`: User registration page
*   `/report`: Waste reporting page

### Building and Running

1.  **Navigate to the frontend directory:**
    ```bash
    cd FRONTEND/waste-track-frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    ng serve
    ```
    The frontend will be available at `http://localhost:4200/`.

4.  **Build for production:**
    ```bash
    ng build
    ```
    The build artifacts will be stored in the `dist/` directory.

### Running Unit Tests

```bash
ng test
```
