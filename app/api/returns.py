import math

from fastapi import APIRouter, HTTPException

from app.models import ReturnNpsIndexRequest
from app.utils import investment_projection_engine


router = APIRouter()

@router.post(":nps")
def calculate_nps_index(request: ReturnNpsIndexRequest):
    try:
        total_transaction_amount = 0
        total_ceiling_amount = 0
        for transaction in request.transaction:
            if transaction.amount < 0:
                continue
            total_transaction_amount += transaction.amount
            total_ceiling_amount += math.ceil(transaction.amount / 100) * 100
        result = investment_projection_engine(payload=request, mode="nps")
        return {"totalTransactionAmount": total_transaction_amount, "totalCeilingAmount": total_ceiling_amount, "savingsByDates": result}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
@router.post(":index")
def calculate_performance_index(request: ReturnNpsIndexRequest):
    try:
        total_transaction_amount = 0
        total_ceiling_amount = 0
        for transaction in request.transaction:
            if transaction.amount < 0:
                continue
            total_transaction_amount += transaction.amount
            total_ceiling_amount += math.ceil(transaction.amount / 100) * 100
        result = investment_projection_engine(payload=request, mode="index")
        return {"totalTransactionAmount": total_transaction_amount, "totalCeilingAmount": total_ceiling_amount, "savingsByDates": result}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))