from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.adapters.routers import (customer_router, 
                                    vehicle_router, 
                                    inventory_part_router, 
                                    repair_order_router, 
                                    repair_order_part_router, 
                                    repair_order_optimization_router)

app = FastAPI(
    title="Autoparts Service API",
    description="Autoparts API documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In order to allow all origins to test the API
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(customer_router.router)
app.include_router(vehicle_router.router)
app.include_router(inventory_part_router.router)
app.include_router(repair_order_router.router)
app.include_router(repair_order_part_router.router)
app.include_router(repair_order_optimization_router.router)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")