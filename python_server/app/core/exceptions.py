from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from core.logging import logger

class AppError(Exception):
    """Custom exception matching the Node.js AppError pattern."""
    def __init__(self, message: str, status_code: int = 400, errors: list = None):
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(self.message)

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.error(f"{request.method} {request.url} - {exc.message}", extra={"status_code": exc.status_code})
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "success": False,
            "message": exc.message,
            "errors": exc.errors,
            "data": None
        }
    )

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled Exception: {request.method} {request.url} - {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "success": False,
            "message": "Internal Server Error",
            "errors": [str(exc)],
            "data": None
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    logger.warning(f"Validation Error: {request.method} {request.url} - {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "success": False,
            "message": "Validation Error",
            "errors": errors,
            "data": None
        }
    )
