# Web Era: AI To-Do App

## Overview
This is the web version of the AI To-Do App, featuring a modern Next.js frontend with FastAPI backend, PostgreSQL database, and authentication.

## Architecture
- **Frontend**: Next.js 16+ with App Router, Tailwind CSS, and Shadcn UI
- **Backend**: Python FastAPI with SQLModel ORM
- **Database**: PostgreSQL (Neon Serverless in production, SQLite for development)
- **Authentication**: JWT-based with custom authentication system

## Features
- User registration and authentication
- Create, read, update, and delete to-dos
- Mark to-dos as complete/incomplete
- Set priorities and categories
- User data isolation

## Project Structure
```
├── frontend/           # Next.js frontend application
│   ├── app/           # App Router pages
│   ├── src/
│   │   ├── context/   # React context providers
│   │   ├── lib/       # Utility functions
│   └── ...
├── backend/           # FastAPI backend application
│   ├── app/
│   │   ├── api/       # API route handlers
│   │   ├── models/    # Data models
│   │   ├── services/  # Business logic
│   │   ├── core/      # Core utilities
│   │   └── db/        # Database configuration
│   ├── main.py        # Main application entry point
│   └── ...
└── specs/web-era/     # Web Era specifications and documentation
```

## Running the Application

### Prerequisites
- Node.js 18+ for frontend
- Python 3.12+ for backend
- npm or yarn for frontend dependencies

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server: `python start_server.py`
4. The API will be available at `http://localhost:8000`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. The web app will be available at `http://localhost:3000`

### Environment Variables
For the backend, create a `.env` file in the backend directory:
```
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key
```

For the frontend, ensure the `.env.local` file contains:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Log in a user
- `GET /api/todos` - Get all user's todos
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo
- `PATCH /api/todos/{id}/complete` - Toggle todo completion

## Authentication
The application uses JWT-based authentication. After login, the token is stored in localStorage and included in the Authorization header for protected API requests.

## Database Schema
- **users**: Stores user information (id, email, password_hash, timestamps)
- **todos**: Stores todo items (id, user_id, title, description, completed, priority, due_date, category, timestamps)

## Development
Both frontend and backend support hot reloading for faster development cycles.