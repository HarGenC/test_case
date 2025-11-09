from enum import Enum
from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT",
    WITHDRAW = "WITHDRAW"


class OperationIn(BaseModel):
    operation_type: OperationType
    amount: Annotated[int, Field(gt=0)]


class WalletCreate(BaseModel):
    balance: int = 0


class WalletOut(BaseModel):
    uuid: UUID
    balance: int