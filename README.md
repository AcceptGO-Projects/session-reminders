# Automatic Reminder System

This project implements an automatic reminder system for users enrolled in various courses. The system is built using FastAPI and SQLAlchemy, and leverages Twilio for sending WhatsApp notifications. The project follows a modular architecture with clearly separated layers for models, repositories, services, and API endpoints.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration with course enrollment
- Course management (create, read, update, delete)
- Reminder management for courses
- Automatic WhatsApp notifications using Twilio
- Modular architecture following best practices

## Architecture

The project structure is organized as follows:

```plaintext
app
├── api
│ ├── endpoints
│ │ ├── courses.py
│ │ ├── reminders.py
│ │ └── users.py
│ └── routes.py
├── config
│ ├── data_source.py
│ └── settings.py
├── models
│ ├── course.py
│ ├── reminder.py
│ ├── user.py
│ ├── user_course.py
│ └── user_reminder.py
├── repositories
│ ├── course_repository.py
│ ├── reminder_repository.py
│ └── user_repository.py
├── schemas
│ ├── course.py
│ ├── reminder.py
│ └── user.py
├── services
│ ├── course_service.py
│ ├── reminder_service.py
│ ├── scheduler_service.py
│ └── user_service.py
└── utils
├── notifications
│ ├── strategies
│ │ ├── init.py
│ │ ├── base.py
│ │ ├── notification_type.py
│ │ └── whatsapp.py
│ └── notification_manager.py
```

## Setup

### Prerequisites

- Python 3.9+
- Virtualenv (optional but recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/automatic-reminder-system.git
   cd automatic-reminder-system
   ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Create a .env file in the root directory and add the following variables:

    ```plaintext
    DB_ENGINE=postgresql+asyncpg
    DB_USER=myuser
    DB_PASSWORD=mypassword
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=mydatabase
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_WHATSAPP_FROM=your_twilio_whatsapp_from
    ```

### Usage
Running the Application
Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.

Scheduler Service
The scheduler service will start automatically with the application. It will handle sending reminders based on the due dates specified.

License
This project is licensed under the MIT License.




