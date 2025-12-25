
from datetime import datetime

from sqlmodel import Relationship, SQLModel, Field

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
    transactions: list["Transaction"] = Relationship(back_populates="customer")  # Relationship to transactions


# Transaction Models
# =====================================================   

class TransactionBase(SQLModel):
    amount: float
    description: str

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer : Customer = Relationship(back_populates="transactions")  # Relationship to customer
     
class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass


# Invoice Models
# =====================================================
class Invoice(SQLModel):
    id: int
    customer: Customer
    transactions: list[Transaction] 
    total: float
    date: datetime = datetime.now()
    
    @property
    def total_amount(self) -> float:
        return sum(t.amount for t in self.transactions)

