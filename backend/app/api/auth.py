from fastapi import APIRouter

router = APIRouter()

# Note: Login and register endpoints have been removed as Better Auth
# handles authentication on the frontend side. The backend now only
# validates session tokens created by Better Auth.