# SQL-Based Real Estate Management System

A full-stack real estate management application built with a PostgreSQL database, FastAPI backend, and HTML/JavaScript frontend. Developed as a university group project for the Mathematical Engineering department at Yıldız Technical University.

---

## Features

- **Role-based access control** — three roles: `admin`, `manager`, and `agent`, each with different permissions
- **JWT authentication** — secure login with token-based session management
- **Property management** — create, list, update, and manage real estate listings
- **User management** — admin-controlled user creation and role assignment
- **Relational database design** — normalized PostgreSQL schema with proper foreign key constraints
- **RESTful API** — all operations exposed via FastAPI endpoints

---

## Tech Stack

| Layer      | Technology           |
|------------|----------------------|
| Database   | PostgreSQL           |
| Backend    | FastAPI (Python)     |
| Auth       | JWT (JSON Web Tokens)|
| Frontend   | HTML, CSS, JavaScript|
| ORM/DB     | psycopg2 / raw SQL   |

---

## Project Structure

```
SQL-Based-Real-Estate-Management-System/
├── backend/
│   ├── main.py            # FastAPI app entrypoint
│   ├── auth.py            # JWT authentication logic
│   ├── database.py        # DB connection and seeding
│   ├── models.py          # Pydantic models / schemas
│   └── routers/           # Route handlers by resource
├── frontend/
│   ├── index.html         # Login page
│   ├── dashboard.html     # Main dashboard
│   └── assets/            # CSS and JS files
├── sql/
│   ├── schema.sql         # Database schema
│   └── seed.sql           # Initial seed data
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 14+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/kagannonem/SQL-Based-Real-Estate-Management-System.git
cd SQL-Based-Real-Estate-Management-System
```

### 2. Set up the database

Create a PostgreSQL database and run the schema and seed scripts:

```bash
psql -U postgres -c "CREATE DATABASE realestate;"
psql -U postgres -d realestate -f sql/schema.sql
psql -U postgres -d realestate -f sql/seed.sql
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/realestate
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive API docs: `http://localhost:8000/docs`

---

## User Roles

| Role    | Capabilities                                      |
|---------|---------------------------------------------------|
| Admin   | Full access — manage users, roles, all listings   |
| Manager | Manage listings, view all agents and their data   |
| Agent   | View and manage their own assigned listings only  |

---

## API Overview

| Method | Endpoint              | Description                  | Auth Required |
|--------|-----------------------|------------------------------|---------------|
| POST   | `/auth/login`         | Login and receive JWT token  | No            |
| GET    | `/users/`             | List all users               | Admin         |
| POST   | `/users/`             | Create a new user            | Admin         |
| GET    | `/properties/`        | List all properties          | Yes           |
| POST   | `/properties/`        | Add a new property           | Manager+      |
| PUT    | `/properties/{id}`    | Update a property            | Manager+      |
| DELETE | `/properties/{id}`    | Delete a property            | Admin         |

---

## Database Schema

The schema follows a normalized relational design. Key tables include:

- `users` — stores user credentials and roles
- `properties` — real estate listings with status, type, and pricing
- `agents` — agent profiles linked to users
- `assignments` — maps agents to properties

See Real Estate Management System Milestone Report for the full schema definition.

---

## Development Notes

- The database is seeded automatically on first run if the seed script is applied.
- Passwords are hashed using `bcrypt` before storage.
- CORS is configured to allow the frontend to communicate with the API during development.

---

## Contributing

This is a university group project. Contributions from team members should be made via feature branches and pull requests targeting `main`.

---

## Project Presentation (Youtube)

https://youtu.be/PeJ8YyknqnI
