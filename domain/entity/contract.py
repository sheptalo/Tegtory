from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ContractStatus(Enum):
    CREATED = "created"
    DELIVERED = "delivered"
    FINISHED = "finished"
    EXPIRED = "expired"


class BaseContract(BaseModel):
    id: int
    status: ContractStatus
    estimated_date: datetime
    created_at: datetime = datetime.now()
