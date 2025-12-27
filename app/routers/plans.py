
from fastapi import APIRouter
from sqlmodel import select

from models import Plan
from db import session_dependency

router = APIRouter()

@router.get("/plans")
async def get_plans(session: session_dependency):
    return session.exec( select(Plan) ).all()
    

@router.post("/plans")
async def create_plan(plan_data: Plan, session: session_dependency):
    plan_db = Plan.model_validate( plan_data.model_dump() )
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db