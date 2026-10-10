# Job Portal API

A Job Portal web application built using Python, Django, and Django REST Framework. It allows job seekers to find jobs and apply for them, while employers can post jobs and manage applications.

## Features

### Job Seeker
- User registration and login
- Browse available jobs
- View job details
- Apply for jobs
- View personal job applications
- Check application status

### Employer
- Employer dashboard
- Post new jobs
- View posted jobs
- Edit job information
- View applicants
- Accept or reject applications

### API
- Company API
- Category API
- Job API
- Application API
- User registration and login API

## Technologies Used

- Python
- Django
- Django REST Framework
- HTML
- CSS
- SQLite
- Git and GitHub

## Project Structure

```text
Job-Portal-API/
├── config/
├── jobs/
├── users/
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/tonwi9046/Job-Portal-API.git
cd Job-Portal-API
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open the website at:

`http://127.0.0.1:8000/`

Django Admin:

`http://127.0.0.1:8000/admin/`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET, POST | `/api/companies/` | List or create companies |
| GET, POST | `/api/categories/` | List or create categories |
| GET, POST | `/api/jobs/` | List or create jobs |
| GET | `/api/jobs/<id>/` | Retrieve job details |
| PUT, PATCH, DELETE | `/api/jobs/<id>/` | Update or delete an authorized job |
| GET, POST | `/api/applications/` | List or create applications |
| GET, DELETE | `/api/applications/<id>/` | Retrieve or delete an authorized application |

Some API operations require authentication and appropriate permissions.

## Team Members

- Faria Islam
- Tonwi

## Purpose

This project was developed as an academic project to practice web development, Django, REST APIs, database management, and Git collaboration.