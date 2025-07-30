import os
import sys
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

# Set up logging
project_root = os.path.dirname(os.getcwd())
sys.path.insert(0, str(project_root))
from app import agent, rag, retrieve
from configs.logger import get_logger_app, setup_logging

from .metrics import LATENCY_HIST, REQUEST_COUNTER

setup_logging()
logger = get_logger_app()

app = FastAPI()

app.include_router(retrieve.router)
app.include_router(rag.router)
app.include_router(agent.router)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {"status": "healthy", "service": "AI Legal Assistant"}


# Root endpoint
@app.get("/")
async def app_root():
    """Root endpoint with service information"""
    return {
        "service": "AI Legal Assistant",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "retrieve": "/retrieve",
            "rag": "/rag",
            "agent": "/agent",
        },
    }


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Middleware to scrape metrics
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    path = request.url.path
    method = request.method
    status_code = response.status_code

    REQUEST_COUNTER.labels(method=method, endpoint=path, http_status=status_code).inc()
    LATENCY_HIST.labels(method=method, endpoint=path).observe(process_time)


# Exception handler for validation error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    logger.info("An error occured: %s", exc.errors())
    errors = [
        {
            "field": ".".join(str(loc) for loc in err["loc"][1:]),  # loại bỏ 'body'
            "error": err["msg"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "message": "Input data is not valid",
                "fields": errors,
            }
        },
    )
