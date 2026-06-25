from fastapi import FastAPI

app = FastAPI(
    title="Smart Temple Backend",
    description="Backend API for Smart Temple Solution using AI, IoT, and Data Analytics.",
    version="1.0.0"
)

@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify backend is running."""
    return {"status": "ok", "message": "Smart Temple Backend is up and running!"}

@app.get("/api/auth/login")
async def stub_login():
    """Stub login endpoint for validation."""
    return {"status": "success", "token": "stub_jwt_token_12345"}
