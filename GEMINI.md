# Gemini Code Assistant Context - Finanpy

This document provides a comprehensive overview of the Finanpy project for the Gemini AI assistant. It is based on an analysis of the project's structure, documentation, and configuration files.

## Project Overview

Finanpy is a full-stack, monolithic web application for personal finance management. It is built with Python and the Django framework, focusing on simplicity, usability, and a clean, dark-themed user interface. The UI is presented in Brazilian Portuguese (pt-BR).

The project is structured into modular Django apps, each handling a specific domain:
-   `core`: Global settings, main views (dashboard, home), and static files.
-   `users`: Manages the custom user model, authentication (login/signup), and sessions.
-   `profiles`: Extends the user model with additional personal information.
-   `accounts`: Manages user bank accounts (e.g., checking, savings).
-   `categories`: Manages user-defined categories for income and expenses.
-   `transactions`: Manages individual financial transactions and links them to accounts and categories.

The project also contains extensive documentation in the `docs/` directory and high-level requirements in `PRD.md`.

### Key Technologies

-   **Backend**: Python 3.13+, Django 5.x
-   **Database**: SQLite (default)
-   **Frontend**: Django Template Language, TailwindCSS (via CDN), Chart.js
-   **Containerization**: Docker, Docker Compose
-   **Dependencies**: See `requirements.txt` for a full list of Python packages.

## Building and Running

There are two primary ways to run the project: using Docker or setting up a local Python environment.

### 1. Running with Docker (Recommended)

This is the simplest way to get the application running, as it handles all dependencies and configurations.

```bash
# Build and start the web service in the background
docker-compose up --build -d

# View the application logs
docker-compose logs -f web

# Stop the service
docker-compose down
```
The application will be available at `http://localhost:8000`.

### 2. Running Locally

This method requires a local Python environment.

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Run the development server
python manage.py runserver
```
The application will be available at `http://localhost:8000`.

## Development Conventions

The project follows a set of established conventions, as detailed in `PRD.md` and `docs/conventions.md`.

-   **Language**:
    -   All user-facing UI text is in Brazilian Portuguese (`pt-BR`).
    -   All code, comments, and documentation are in English.
-   **Coding Style**:
    -   Follows PEP 8 guidelines.
    -   Uses single quotes (`'`) in Python code where possible.
-   **Django Practices**:
    -   Prefers Class-Based Views (CBVs) over function-based views.
    -   Uses a custom user model (`users.User`) with email as the primary identifier.
    -   Organizes business logic into the corresponding Django apps.
    -   Uses Django's signal framework (`signals.py`) for decoupled logic, such as automatically creating a `Profile` when a `User` is created.
-   **Testing**:
    -   Tests are expected for new features and bug fixes.
    -   The testing framework is built on Django's standard `TestCase` or `pytest`.
    -   Run tests using `python manage.py test`.
