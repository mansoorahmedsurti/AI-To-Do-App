from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import auth, todos
from app.db.init_db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    create_db_and_tables()
    yield


app = FastAPI(title="AI To-Do App API", version="1.0.0", lifespan=lifespan)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI To-Do App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}