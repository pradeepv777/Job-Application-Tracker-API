# Job Application Tracker - Backend API

![Tests](https://github.com/pradeepv777/Job-Application-Tracker-Backend/actions/workflows/test.yml/badge.svg)

A **FastAPI** backend that helps job seekers organize and manage their entire placement journey. Track applications, interviews, resumes, and get analytics - all through a clean REST API.

---

## Project Overview

Instead of maintaining spreadsheets or scattered notes, this application provides a centralized REST API to manage:

- **Job Applications** - Track company, role, salary, and status
- **Interviews** - Schedule and record interview rounds
- **Resume Management** - Upload and manage PDF resumes
- **Dashboard** - Summary statistics of your job search
- **Analytics** - Salary insights, success rate, and interview metrics

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Framework | FastAPI 0.141.1 |
| Language | Python 3.13 |
| Database | PostgreSQL 17 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Authentication | JWT (python-jose) |
| Password Hashing | Passlib (bcrypt) |
| Server | Uvicorn |
| Containerization | Docker + Docker Compose |

---

## Features

- JWT authentication (register, login, protected routes)
- Full CRUD for job applications with pagination, search, sort, and filter
- Interview tracking per application
- Resume upload, download, and delete (PDF only)
- Dashboard with application status breakdown
- Analytics with salary stats, success rate, and interview counts

---

## Prerequisites

- Python 3.8+ and pip, **or** Docker and Docker Compose

---

## Running with Docker (Recommended)

This is the easiest way to run the full stack including PostgreSQL.

### 1. Clone the repository
```bash
git clone https://github.com/pradeepv777/Job-Application-Tracker-Backend.git
cd Job-Application-Tracker-Backend
```

### 2. Configure environment variables
Copy the example file and fill in your values:
```bash
cp .env.example .env
```

`.env` should contain:
```env
DATABASE_URL=postgresql+psycopg://postgres:root@db:5432/job_application_tracker
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Build and start the containers
```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`

### 4. Run database migrations
```bash
docker compose exec api alembic upgrade head
```

### Stop the containers
```bash
docker compose down
```

---

## Running Locally (Without Docker)

### 1. Clone the repository
```bash
git clone https://github.com/pradeepv777/Job-Application-Tracker-Backend.git
cd Job-Application-Tracker-Backend
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/job_application_tracker
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start the development server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## API Documentation

Once the server is running:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login and get JWT token | No |

### Applications
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/applications` | Create new application | Yes |
| GET | `/applications` | Get all applications (paginated, filterable) | Yes |
| GET | `/applications/{id}` | Get application by ID | Yes |
| PUT | `/applications/{id}` | Update application | Yes |
| DELETE | `/applications/{id}` | Delete application | Yes |

**Query parameters for GET /applications:**
- `search` - Filter by company name
- `status` - Filter by status
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 10, max: 100)
- `sort_by` - Sort field: id, company, salary, status (default: id)
- `order` - Sort order: asc, desc (default: asc)

### Interviews
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/interviews` | Create interview for an application | Yes |
| GET | `/interviews/application/{id}` | Get all interviews for an application | Yes |
| PUT | `/interviews/{id}` | Update interview | Yes |
| DELETE | `/interviews/{id}` | Delete interview | Yes |

### Resume
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/resume/upload` | Upload PDF resume | Yes |
| GET | `/resume` | Get resume metadata | Yes |
| GET | `/resume/download` | Download resume file | Yes |
| DELETE | `/resume` | Delete resume | Yes |

### Dashboard
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/dashboard` | Get application stats by status | Yes |

### Analytics
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/analytics` | Get salary stats, status breakdown, interview metrics, and success rate | Yes |

---

## Project Structure

```
JobApplicationTracker-Backend/
├── app/
│   ├── auth/
│   │   ├── dependencies.py     # JWT token dependency injection
│   │   ├── hashing.py          # bcrypt password hashing
│   │   └── jwt_handler.py      # Token creation and verification
│   ├── models/
│   │   ├── user.py
│   │   ├── application.py
│   │   └── interview.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── application.py
│   │   ├── interview.py
│   │   ├── resume.py
│   │   ├── dashboard.py
│   │   └── analytics.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── application.py
│   │   └── interview.py
│   ├── config.py               # Environment variable settings
│   ├── database.py             # SQLAlchemy engine and session
│   ├── enums.py                # ApplicationStatus and InterviewResult enums
│   └── main.py                 # FastAPI app, middleware, router registration
├── alembic/
│   └── versions/               # Migration files
├── uploads/
│   └── resumes/                # Uploaded PDF files
├── .env                        # Environment variables (not committed)
├── .env.example                # Environment variable template
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Database Schema

### users
| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| name | String | Required |
| email | String | Unique, required |
| hashed_password | String | bcrypt hashed |
| resume_path | String | Nullable |

### applications
| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| user_id | Integer | FK to users |
| company | String | Required |
| role | String | Required |
| salary | Integer | Required, > 10000 |
| status | String | Applied / Interview / Offer / Rejected |

### interviews
| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| application_id | Integer | FK to applications |
| round | String | e.g. Technical Round 1 |
| date | Date | Interview date |
| time | Time | Interview time |
| interviewer | String | |
| notes | String | |
| result | String | Scheduled / Completed / Cancelled |

---

## Authentication Flow

1. Register with name, email, and password
2. Password is hashed with bcrypt before storing
3. Login returns a JWT access token
4. Include the token in all protected requests: `Authorization: Bearer <token>`
5. Token is verified on every protected route

---

## Application Statuses

| Status | Description |
|--------|-------------|
| Applied | Application submitted |
| Interview | Interview stage |
| Offer | Offer received |
| Rejected | Application rejected |

---

## License

This project is open source and available under the MIT License.

## Author

**Pradeep**
- GitHub: [@pradeepv777](https://github.com/pradeepv777)
