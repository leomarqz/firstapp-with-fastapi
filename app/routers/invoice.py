
from fastapi import APIRouter, Depends, HTTPException

from models import Invoice

router = APIRouter()

@router.post("/invoices")
async def create_invoice(invoice: Invoice):
    return {
        "message": "Invoice created successfully",
        "invoice": invoice
    }