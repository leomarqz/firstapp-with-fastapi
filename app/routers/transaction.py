
from fastapi import APIRouter, HTTPException, status as Status
from sqlmodel import select

from models import Customer, Transaction, TransactionCreate
from db import session_dependency

router = APIRouter()

@router.get("/transactions")
async def get_transactions(session: session_dependency):
    return session.exec( select(Transaction) ).all()

@router.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: int, session: session_dependency):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=Status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    return transaction_db

@router.post("/transactions", status_code=Status.HTTP_201_CREATED, response_model=Transaction)
async def create_transaction(transaction_data: TransactionCreate, session: session_dependency): 
    transaction_data_dict: dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id") )
    
    if not customer:
        raise HTTPException(status_code=Status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist!")
    
    transaction_db = Transaction.model_validate( transaction_data_dict )
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    
    return transaction_db