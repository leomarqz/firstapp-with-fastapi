
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, create_engine, Session

from contextlib import asynccontextmanager

DATABASE_NAME: str = "db.sqlite3"
DATABASE_URL: str = f"sqlite:///{DATABASE_NAME}"

engine = create_engine(
    url  =DATABASE_URL,  #connection string to postgresql
    echo =True, # log SQL queries
    pool_pre_ping=True # check if connection is alive
    )

@asynccontextmanager
async def update_database(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield 

def get_db_session():
    with Session(engine) as session:
        yield session
        
session_dependency = Annotated[Session, Depends(get_db_session)]
