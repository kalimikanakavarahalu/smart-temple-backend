from fastapi import FastAPI
from src.api.routes import router as api_router
from src.api.auth import router as auth_router

app = FastAPI(
    title="Smart Temple Backend",
    description="Backend API for Smart Temple Solution using AI, IoT, and Data Analytics.",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(api_router, prefix="/api", tags=["Modules"])

@app.get("/api/health")  
async def health_check():
    """Health check endpoint to verify backend is running."""
    return {"status": "ok", "message": "Smart Temple Backend is up and running!"}

