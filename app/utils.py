from datetime import datetime
import math
from bisect import bisect_left, bisect_right

from app.models import ReturnNpsIndexResponse

def calculate_ceiling_and_remanent(amount: float):
    """
    This function calculates the ceiling and remanent for a given transaction amount.
    """
    ceiling = math.ceil(amount / 100) * 100
    remanent = ceiling - amount
    return ceiling, remanent


def apply_q_rule(transactions, remanents, q_periods):
    """
    This function applies the Q rule to the remanents based on the provided Q periods.
    It sorts the Q periods by their start date and uses binary search to find the applicable Q period for each transaction, updating the remanent to the fixed value if the transaction falls within a Q period.
    """
    q_sorted = sorted(q_periods, key=lambda q: q.start)
    q_starts = [q.start for q in q_sorted]

    for i, txn in enumerate(transactions):
        idx = bisect_right(q_starts, txn.date) - 1

        if idx >= 0:
            q = q_sorted[idx]
            if q.start <= txn.date <= q.end:
                remanents[i] = q.fixed

    return remanents


def apply_p_rule(transactions, remanents, p_periods):
    """
    This function applies the P rule to the remanents based on the provided P periods. 
    It creates events for the start and end of each P period, sorts them, and then iterates through the transactions to adjust the remanents according to the running extra amount from the active P periods.
    """

    # Create events
    events = []
    for p in p_periods:
        events.append((p.start, p.extra))
        events.append((p.end, -p.extra))

    events.sort(key=lambda x: x[0])

    running_extra = 0
    event_index = 0

    for i, txn in enumerate(transactions):
        while event_index < len(events) and events[event_index][0] <= txn.date:
            running_extra += events[event_index][1]
            event_index += 1

        remanents[i] += running_extra

    return remanents


def calculate_tax(income: float) -> float:
    """
    Calculate tax based on the provided income slabs.
    """
    tax = 0

    if income <= 700000:
        return 0

    if income > 1500000:
        tax += (income - 1500000) * 0.30
        income = 1500000

    if income > 1200000:
        tax += (income - 1200000) * 0.20
        income = 1200000

    if income > 1000000:
        tax += (income - 1000000) * 0.15
        income = 1000000

    if income > 700000:
        tax += (income - 700000) * 0.10

    return tax


def investment_projection_engine(payload: dict, mode: str):
    """
    cal the projection of investments based on the remanents and the rules provided in the payload.
    calculates the future value of investments at the end of K periods, adjusted for inflation, and computes the profit and tax benefits (if applicable).
    """

    wage = payload.wage
    age = payload.age
    inflation = payload.inflation
    years = 60 - age

    if years <= 0:
        return []

    transactions = sorted(payload.transaction, key=lambda x: x.date)

    q_periods = payload.q if hasattr(payload, 'q') else []
    p_periods = payload.p if hasattr(payload, 'p') else []
    k_periods = payload.k if hasattr(payload, 'k') else []

    # Step 1: base remanent
    dates = []
    remanents = []

    for txn in transactions:
        dates.append(txn.date)
        ceil_val = math.ceil(txn.amount / 100) * 100
        remanents.append(ceil_val - txn.amount)

    # Step 2: Q rule
    remanents = apply_q_rule(transactions, remanents, q_periods)

    # Step 3: P rule
    remanents = apply_p_rule(transactions, remanents, p_periods)

    # Step 4: K grouping + projection
    if mode == "nps":
        rate = 0.0711
    else:
        rate = 0.1449
    results = []

    for k in k_periods:
        l = bisect_left(dates, k.start)
        r = bisect_right(dates, k.end)
        invested = sum(remanents[l:r])

        future_value = invested * ((1 + rate) ** years)
        real_value = future_value / ((1 + inflation / 100) ** years)
        profit = real_value - invested

        # Tax benefit only for NPS
        tax_benefit = 0
        if mode == "nps":
            eligible = min(invested, wage * 0.10, 200000)
            tax_before = calculate_tax(wage)
            tax_after = calculate_tax(wage - eligible)
            tax_benefit = tax_before - tax_after

        results.append(ReturnNpsIndexResponse(
            start=k.start,
            end=k.end,
            profit=round(profit, 2),
            taxBenefit=round(tax_benefit, 2),
            amount=invested
        ))

    return results