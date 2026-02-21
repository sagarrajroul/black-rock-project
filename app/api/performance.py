from fastapi import APIRouter
from ..models import PerformanceResponse
import time
import psutil
import threading


router = APIRouter()

@router.get("", response_model=PerformanceResponse)
def get_performance_metrics():
    start_time = time.perf_counter()

    # Memory usage (current process)
    process = psutil.Process()
    memory_usage_mb = process.memory_info().rss / (1024 * 1024)

    # Active thread count
    thread_count = threading.active_count()

    response_time_ms = (time.perf_counter() - start_time) * 1000

    return PerformanceResponse(
        response_time_ms=round(response_time_ms, 2),
        memory_usage_mb=round(memory_usage_mb, 2),
        thread_count=thread_count
    )
