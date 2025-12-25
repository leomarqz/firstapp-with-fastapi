
from fastapi import APIRouter, Depends, HTTPException

from models import Transaction

router = APIRouter()

@router.post("/transactions")
async def create_transaction(transaction: Transaction):
    return {
        "message": "Transaction created successfully",
        "transaction": transaction
    }