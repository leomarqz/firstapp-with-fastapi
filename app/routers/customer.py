
from fastapi import APIRouter, HTTPException, status as Status

from models import Customer, CustomerCreate, CustomerUpdate
from db import session_dependency

from sqlmodel import select

router = APIRouter()


@router.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: session_dependency):
    customer = Customer.model_validate( customer_data.model_dump() ) # Create Customer instance from request data
    session.add(customer) # To add the new customer
    session.commit() # To persist the new customer
    session.refresh(customer) # To get the generated ID and other defaults
    return customer # Return the created customer

@router.get("/customers", response_model=list[Customer])
async def get_all_customers(session: session_dependency):
    return session.exec(select(Customer)).all()

@router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, session: session_dependency):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=Status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_db

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=Status.HTTP_201_CREATED)
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: session_dependency):
    customer_db = session.get(Customer, customer_id) 
    if not customer_db:
        raise HTTPException(status_code=Status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data_dict = customer_data.model_dump(exclude_unset=True) # Exluye campos vacios o nulos y actualiza solo los proporcionados
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, session: session_dependency):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=Status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return {"detail": "Customer deleted successfully"}