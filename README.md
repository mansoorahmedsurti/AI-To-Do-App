# AI To-Do App - Phase 2

## Architecture Overview

This project implements a modern web application with strict compliance to Hackathon Phase 2 requirements:

- **Frontend**: Next.js 16+ with Better Auth for authentication
- **Backend**: FastAPI with PostgreSQL database
- **Authentication**: Better Auth (TypeScript/Next.js library) with direct database integration
- **Database**: PostgreSQL only (no fallbacks)

## Key Changes from Previous Version

### Database Strictness
- Removed all SQLite fallbacks
- Application will crash if `DATABASE_URL` is not set
- Enforced PostgreSQL connection using `asyncpg` or `psycopg2`

### Authentication Migration
- **Frontend**: Uses Better Auth with PostgreSQL adapter
- **Backend**: No longer issues tokens; only validates session tokens created by Better Auth
- Removed old `/auth/login` and `/auth/register` endpoints
- Backend verifies session tokens against the database

## Project Structure
```
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes (auth, todos)
│   │   ├── models/      # Data models (user, todo, session)
│   │   ├── services/    # Business logic
│   │   ├── core/        # Configuration and auth utilities
│   │   └── db/          # Database configuration
│   └── main.py          # Application entry point
├── frontend/             # Next.js frontend
│   ├── app/             # App Router pages
│   ├── lib/             # Utilities (auth, api)
│   └── ...              # Other Next.js files
├── docker-compose.yml    # PostgreSQL container configuration
└── .env.example         # Environment variables example
```

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.12+

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Start PostgreSQL: `docker-compose up -d`
5. Start the server: `python start_server.py`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Set up environment variables (see `.env.example`)
4. Start the development server: `npm run dev`

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todos
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BASE_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-better-auth-secret
```

## API Endpoints

### Todo Endpoints (require authentication)
- `GET /api/todos` - Get all user's todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo
- `PATCH /api/todos/{id}/complete` - Toggle todo completion

### Auth Endpoints
- Authentication is handled by Better Auth on the frontend
- Backend only validates session tokens created by Better Auth

## Database Schema
- **users**: Stores user information (id, email, password_hash, timestamps)
- **todos**: Stores todo items (id, user_id, title, description, completed, priority, due_date, category, timestamps)
- **sessions**: Stores Better Auth session information (id, token, user_id, expires_at, timestamps)

## Development
Both frontend and backend support hot reloading for faster development cycles.