from bisect import bisect_left, bisect_right
import math

from fastapi import APIRouter, HTTPException
from typing import List
from ..models import (TransactionInvalidResponse, TransactionParseRequest, TransactionParseResponse, 
                      TransactionValidateRequest, TransactionFilterRequest, FilteredTransactionResponse)
from ..utils import apply_p_rule, apply_q_rule, calculate_ceiling_and_remanent


router = APIRouter()

@router.post(":parse", response_model=List[TransactionParseResponse])
def parse_transactions(transactions: List[TransactionParseRequest]):
    try:
        result = []

        for transaction in transactions:
            ceiling, remanent = calculate_ceiling_and_remanent(transaction.amount)

            result.append(
                TransactionParseResponse(
                    date=transaction.date,
                    amount=transaction.amount,
                    ceiling=ceiling,
                    remanent=remanent
                )
            )

        return result
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@router.post(":validate")
def validate_transactions(request: TransactionValidateRequest):
    try:
        valid = []
        invalid = []
        seen_before = {}
        for transaction in request.transaction:
            if transaction.amount<0:
                invalid.append(TransactionInvalidResponse(
                        date=transaction.date,
                        amount=transaction.amount,
                        message="negative amounts are not allowed"
                    ))
            elif seen_before.get(transaction.date) == transaction.amount:
                invalid.append(TransactionInvalidResponse(
                        date=transaction.date,
                        amount=transaction.amount,
                        message="Duplicate transactions"
                    ))
            else:
                seen_before[transaction.date] = transaction.amount
                valid.append(transaction)
        return {"valid": valid, "invalid": invalid}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@router.post(":filter")
def filter_transactions(request: TransactionFilterRequest):
    try:
        valid = []
        invalid = []
        seen_before = {}
        for transaction in request.transaction:
            if transaction.amount<0:
                invalid.append(TransactionInvalidResponse(
                        date=transaction.date,
                        amount=transaction.amount,
                        message="negative amounts are not allowed"
                    ))
            elif seen_before.get(transaction.date) == transaction.amount:
                invalid.append(TransactionInvalidResponse(
                        date=transaction.date,
                        amount=transaction.amount,
                        message="Duplicate transactions"
                    ))
            else:
                seen_before[transaction.date] = transaction.amount
                valid.append(transaction)
        transactions_sorted = sorted(valid, key=lambda t: t.date)

        ceil_values = []
        remanents = []

        for txn in transactions_sorted:
            ceil_val = math.ceil(txn.amount / 100) * 100
            ceil_values.append(ceil_val)
            remanents.append(ceil_val - txn.amount)
        q_periods = request.q
        p_periods = request.p
        remanents = apply_q_rule(transactions_sorted, remanents, q_periods)

        remanents = apply_p_rule(transactions_sorted, remanents, p_periods)

        k_periods = request.k
        validate_transactions = []
        for i, txn in enumerate(transactions_sorted):
            in_k_period = any(k.start <= txn.date <= k.end for k in k_periods)
            if remanents[i] == 0:
                continue
            validate_transactions.append(FilteredTransactionResponse(
                date=txn.date,
                amount=txn.amount,
                ceiling=ceil_values[i],
                remanent=remanents[i],
                inKPeriod=in_k_period
            ))
        return {"valid": validate_transactions, "invalid": invalid}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))