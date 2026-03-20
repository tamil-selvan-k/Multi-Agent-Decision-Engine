import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.api.v1.routes import router as v1_router
from app.core.exceptions import (
    AppError, 
    app_error_handler, 
    global_exception_handler,
    validation_exception_handler
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI Microservice for cross-domain enterprise orchestration.",
    version="1.0.0"
)

# Configure CORS (Allow the Node.js Gateway to communicate with this service)
allow_origins_list = ["*"] if settings.CORS_ORIGINS == "*" else [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins_list,
    allow_credentials=False if settings.CORS_ORIGINS == "*" else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/health")
async def health_check():
    return {"status": "AI Microservice is online and ready for delegation."}

app.include_router(v1_router, prefix="/api/v1", tags=["Orchestration"])

if __name__ == "__main__":
    # Explicitly binding the backend to port 3001
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
