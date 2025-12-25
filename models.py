
from datetime import datetime

from pydantic import BaseModel

from sqlmodel import SQLModel, Field

# =====================================================
# MODELS ==============================================
# =====================================================

# Customer Models
# =====================================================
class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: str = Field(default=None, unique=True)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

# Customer model for DB
class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


# Transaction Models
# =====================================================   
class Transaction(SQLModel):
    id: int
    amount: float
    description: str
    
class Invoice(SQLModel):
    id: int
    customer: Customer
    transactions: list[Transaction] 
    total: float
    date: datetime = datetime.now()
    
    @property
    def total_amount(self) -> float:
        return sum(t.amount for t in self.transactions)

