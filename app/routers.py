from fastapi import APIRouter
from app.api.transactions import router as transaction_router
from app.api.performance import router as performance_router
from app.api.returns import router as returns_router
api_router = APIRouter()
api_router.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(performance_router, prefix="/performance", tags=["Performance"])
api_router.include_router(returns_router, prefix="/returns", tags=["Returns"])