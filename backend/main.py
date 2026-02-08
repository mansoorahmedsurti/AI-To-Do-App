from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, todos
from app.db.init_db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    create_db_and_tables()
    yield


app = FastAPI(title="AI To-Do App API", version="1.0.0", lifespan=lifespan)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# Note: Auth router is included but only contains placeholder routes
# Authentication is handled by Better Auth on the frontend
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI To-Do App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}