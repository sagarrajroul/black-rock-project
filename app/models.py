from datetime import datetime
from pydantic import BaseModel, field_serializer, field_validator

from datetime import datetime
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class CustomDateTime:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_plain_validator_function(cls.validate)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "date-time",
            "example": "2026-02-21 06:04:11",
        }

    @classmethod
    def validate(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError('date must be in format "YYYY-MM-DD HH:mm:ss"')

class TransactionParseRequest(BaseModel):
    date: CustomDateTime
    amount: float

class TransactionInvalidResponse(BaseModel):
    date: datetime
    amount: float
    message: str
    
    @field_serializer("date")
    def serialize_datetime(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")


class TransactionParseResponse(TransactionParseRequest):
    ceiling: float
    remanent: float

    @field_serializer("date")
    def serialize_datetime(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

class TransactionValidateRequest(BaseModel):
    wage: float
    transaction: list[TransactionParseResponse]

class TransactionKPeriodRequest(BaseModel):
    start: CustomDateTime
    end: CustomDateTime

class TransactionPPeriodRequest(TransactionKPeriodRequest):
    extra: float
class TransactionQPeriodRequest(TransactionKPeriodRequest):
    fixed: float

class TransactionFilterRequest(BaseModel):
    q: list[TransactionQPeriodRequest]
    p: list[TransactionPPeriodRequest]
    k: list[TransactionKPeriodRequest]
    wage: float
    transaction: list[TransactionParseRequest]


class FilteredTransactionResponse(TransactionParseResponse):
    inKPeriod: bool
    
class ReturnNpsIndexRequest(TransactionFilterRequest):
    age : int
    inflation: float

class ReturnNpsIndexResponse(BaseModel):
    start: datetime
    end: datetime
    amount: float
    profit: float
    taxBenefit: float
    @field_serializer("start")
    def serialize_start_datetime(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("end")
    def serialize_end_datetime(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

class PerformanceResponse(BaseModel):
    response_time_ms: float
    memory_usage_mb: float
    thread_count: int