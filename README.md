<div align="center">

# 🏋️ AI Fitness API

**AI-powered RESTful API for personalized workout and nutrition planning**

Built with FastAPI · Powered by Groq (Llama 3.1) · PostgreSQL · Docker

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.133-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## Overview

AI Fitness API is a full-stack fitness platform that leverages **Large Language Models** to generate fully personalized workout routines and diet plans based on each user's physical profile and goals. Users can modify plans through natural language, log workouts with detailed set/rep tracking, and analyze meals using free-text input — all secured behind JWT authentication.

### Key Highlights

- **AI-Generated Plans** — Workout routines and diet plans are generated dynamically by Groq's Llama 3.1 model, tailored to the user's age, weight, height, experience level, and goals.
- **Natural Language Modification** — Users can refine their plans by describing changes in plain text (e.g., *"replace bench press with dumbbell press"*).
- **Smart Meal Logging** — Describe what you ate in free text and the AI automatically estimates calories and macronutrients.
- **Full CRUD Persistence** — Save, activate, update, and delete workout routines and diet plans.
- **Workout Session Tracking** — Log individual training sessions with per-exercise, per-set granularity (reps, weight).
- **JWT Authentication** — Secure access with token-based auth, including password reset flow.
- **Dockerized Deployment** — One-command deployment with Docker Compose (API + Frontend).

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | FastAPI (Python 3.11) |
| **AI / LLM** | Groq Cloud — Llama 3.1 8B Instant |
| **Database** | PostgreSQL with SQLAlchemy ORM |
| **Migrations** | Alembic |
| **Authentication** | JWT (PyJWT) + bcrypt password hashing |
| **Validation** | Pydantic v2 |
| **Frontend** | Streamlit |
| **Containerization** | Docker & Docker Compose |
| **Server** | Uvicorn (ASGI) |

---

## Architecture

```
ai-fitness-api/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── api/
│   │   ├── deps.py              # Dependency injection (auth, DB session)
│   │   └── routers/
│   │       ├── auth.py          # Login, forgot/reset password
│   │       ├── users.py         # Registration & profile management
│   │       ├── workouts.py      # Workout generation, CRUD & tracking
│   │       └── diets.py         # Diet generation, CRUD & meal logging
│   ├── core/
│   │   ├── config.py            # Environment-based settings (Pydantic)
│   │   ├── database.py          # SQLAlchemy engine & session
│   │   └── security.py          # JWT creation/verification, hashing
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py              # User + password reset tokens
│   │   ├── profile.py           # Physical profile & preferences
│   │   ├── workout.py           # Plans, sessions, exercises, sets
│   │   └── diet.py              # Diet plans & daily meal logs
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── auth.py, token.py    # Auth & token schemas
│   │   ├── user.py, profile.py  # User & profile schemas
│   │   ├── workout.py           # Workout plan schemas
│   │   ├── diet.py              # Diet plan & meal schemas
│   │   └── tracking.py          # Session logging schemas
│   └── services/
│       ├── llm_service.py       # Groq LLM integration layer
│       └── user_service.py      # User data access logic
├── alembic/                     # Database migration scripts
├── views/                       # Streamlit frontend views
├── frontend.py                  # Streamlit app entry point
├── docker-compose.yml           # Multi-container orchestration
├── Dockerfile.backend           # API container
├── Dockerfile.frontend          # Frontend container
└── requirements.txt
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/login` | Authenticate and receive a JWT access token |
| `POST` | `/forgot-password` | Request a password reset token |
| `POST` | `/reset-password` | Reset password using a valid token |

### Users & Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Register a new user account |
| `GET` | `/users/me` | Retrieve the authenticated user's profile |
| `PUT` | `/users/me` | Create or update user profile (age, weight, height, goals) |

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/workouts/generate` | Generate an AI-powered workout plan based on user profile |
| `POST` | `/workouts/modify` | Modify an existing plan using natural language instructions |
| `POST` | `/workouts/save` | Persist a workout plan to the database |
| `GET` | `/workouts/saved` | List all saved workout plans |
| `GET` | `/workouts/active` | Get the currently active workout routine |
| `PUT` | `/workouts/saved/{id}/activate` | Set a saved plan as the active routine |
| `DELETE` | `/workouts/saved/{id}` | Delete a saved workout plan |
| `POST` | `/workouts/log` | Log a completed workout session (exercises, sets, reps, weight) |
| `GET` | `/workouts/history` | Retrieve paginated workout session history |
| `PUT` | `/workouts/history/{id}` | Update a logged workout session |
| `DELETE` | `/workouts/history/{id}` | Delete a logged workout session |

### Diets & Nutrition

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/diets/generate` | Generate an AI-powered diet plan based on user profile |
| `POST` | `/diets/modify` | Modify an existing diet plan using natural language |
| `POST` | `/diets/save` | Persist a diet plan to the database |
| `GET` | `/diets/saved` | List all saved diet plans |
| `GET` | `/diets/active` | Get the currently active diet plan |
| `PUT` | `/diets/saved/{id}/activate` | Set a saved plan as the active diet |
| `DELETE` | `/diets/saved/{id}` | Delete a saved diet plan |
| `POST` | `/diets/log-text` | Analyze a meal described in free text (returns macros) |
| `POST` | `/diets/log` | Analyze and save a meal log to the database |
| `GET` | `/diets/history` | Retrieve paginated meal log history |
| `DELETE` | `/diets/history/{id}` | Delete a meal log entry |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check — returns service status and version |

> All endpoints except `/login`, `/users/`, `/forgot-password`, `/reset-password`, and `/health` require a valid JWT Bearer token.

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- A [Groq API Key](https://console.groq.com/) (free tier available)
- A PostgreSQL instance (or use a cloud provider like [Neon](https://neon.tech/), [Supabase](https://supabase.com/), etc.)

### 1. Clone the Repository

```bash
git clone https://github.com/JavierDeMiguelPerez/ai-fitness-api.git
cd ai-fitness-api
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@host:5432/fitness_db
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
PROJECT_NAME=AI Fitness API
PROJECT_VERSION=1.0.0
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

The services will be available at:

| Service | URL |
|---------|-----|
| **API** | `http://localhost:8000` |
| **API Docs (Swagger)** | `http://localhost:8000/docs` |
| **Frontend** | `http://localhost:8501` |

### Alternative: Local Development

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

---

## Database Migrations

This project uses **Alembic** for database schema migrations:

```bash
# Apply all pending migrations
alembic upgrade head

# Generate a new migration after model changes
alembic revision --autogenerate -m "description of changes"
```

---

## Interactive API Documentation

FastAPI automatically generates interactive documentation. Once the server is running:

- **Swagger UI** — [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc** — [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Example Usage

### Register a new user

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
```

### Authenticate

```bash
curl -X POST http://localhost:8000/login \
  -d "username=user@example.com&password=securepassword"
```

### Generate a workout plan

```bash
curl -X POST http://localhost:8000/workouts/generate \
  -H "Authorization: Bearer <your_token>"
```

### Log a meal with natural language

```bash
curl -X POST http://localhost:8000/diets/log \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"meal_text": "Two eggs, a slice of whole wheat toast, and a glass of orange juice"}'
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built by [Javier De Miguel Pérez](https://www.linkedin.com/in/javiermiguelperez/)**

</div>