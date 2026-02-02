Hi! This is my submission for the URL Shortener backend task.

I built this application using Django and Django REST Framework. The goal was to create a clean, functional URL shortener that handles authentication, URL management, and analytics efficiently. I decided to use a `ModelViewSet` approach to keep the code unified between the API and the UI.

## Features

### Core Functionality
-   **User Authentication**: Secure Sign Up, Login, and Logout functionality.
-   **URL Shortening**: Convert long URLs into compact 6-character short codes using Base62 encoding.
-   **Custom Alias**: Users can optionally pick their own custom short code.
-   **Redirection**: Instant redirection from short URLs to the original destination.

### URL Management
-   **Dashboard**: A centralized hub for users to view all their links.
-   **Edit**: Update the destination URL of existing short links.
-   **Delete**: Remove unwanted short links.
-   **Analytics**: View the total number of clicks for each link.
-   **QR Code Generation**: Automatically generate QR codes for every short link.
-   **Link Expiration**: Set optional expiration times (e.g., 1 day, 1 week) for temporary links.
-   **Custom Short URLs**: Pick your own memorable short codes.

### API Support
The project includes a robust REST API built with Django REST Framework (DRF):
-   **Endpoints**:
    -   `GET /api/urls/`: List your short URLs.
    -   `POST /api/urls/`: Create a new short URL.
    -   `GET /api/urls/{id}/`: Retrieve details of a specific URL.
    -   `PUT/PATCH /api/urls/{id}/`: Update a URL.
    -   `DELETE /api/urls/{id}/`: Delete a URL.
    -   `POST /api/accounts/signup/`: Register a new user via API.
-   The API is fully integrated with the UI views for a seamless code structure.

## Setup Instructions

### Prerequisites
-   Python 3.x installed.

*(Note: I used a virtual environment named `myenv` during development, so I recommend creating one to keep dependencies isolated.)*

### Installation

1.  **Clone the Repository** (or extract the project files):
    ```bash
    git clone <your-repo-link>
    cd assingement
    ```

2.  **Create and Activate Virtual Environment** (Recommended):
    ```bash
    # Windows
    python -m venv myenv
    myenv\Scripts\activate
    


3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Database Migrations**:
    ```bash
    cd core
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a Superuser** (Optional, for Admin Access):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

7.  **Access the Application**:
    -   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Technology Stack
-   **Backend**: Python, Django
-   **API**: Django REST Framework (DRF)
-   **Database**: SQLite (Default)
-   **Frontend**: HTML, CSS (Bootstrap 5)
