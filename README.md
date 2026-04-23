# Productivity App Backend

A Flask-based RESTful API designed to manage personal tasks with full user authentication.

## Features
- **Session-based Authentication**: Secure signup, login, and logout.
- **User-Owned Resources**: Users can only CRUD their own tasks.
- **Pagination**: The task index route supports paginated results.

## Installation & Setup

1. **Install dependencies**:
   pipenv install && pipenv shell

2. **Initialize Database**:
   lask db upgrade

3. **Seed Data**:
   python seed.py

4. **Run Application**:
   python app.py

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /signup | Create a new user |
| POST   | /login  | Authenticate a user |
| DELETE | /logout | Terminate session |
| GET    | /check_session | Verify session |
| GET    | /tasks | List tasks (Paginated) |
| POST   | /tasks | Create a task |
| PATCH  | /tasks/<id> | Update task |
| DELETE | /tasks/<id> | Remove task |