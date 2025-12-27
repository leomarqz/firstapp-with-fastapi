
import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from db import update_database

from .routers.customer import router as customer_router
from .routers.transaction import router as transaction_router
from .routers.invoice import router as invoice_router
from .routers.others import router as others_router
from .routers.plans import router as plans_router

# Initialize FastAPI application with lifespan event for database update
app = FastAPI(lifespan=update_database)

# Include routers with versioned API prefix
app.include_router(customer_router, prefix="/api/v1", tags=["customers"])
app.include_router(plans_router, prefix="/api/v1", tags=["plans"])
app.include_router(transaction_router, prefix="/api/v1", tags=["transactions"])
app.include_router(invoice_router, prefix="/api/v1", tags=["invoices"])
app.include_router(others_router, prefix="/api/v1", tags=["others"])

# Root endpoint providing basic service information
@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI!",
        "status": "active",
        "timestamp": datetime.now(zoneinfo.ZoneInfo("UTC"))
    }
    



