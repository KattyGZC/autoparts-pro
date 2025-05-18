from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.adapters.routers import customer_router, vehicle_router

app = FastAPI(
    title="Autoparts Service API",
    description="Autoparts API documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(customer_router.router)
app.include_router(vehicle_router.router)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")